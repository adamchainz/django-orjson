from __future__ import annotations

import datetime
import decimal
from inspect import getsource
from textwrap import dedent

import django
import pytest
from django.core.serializers.json import DjangoJSONEncoder
from django.test import SimpleTestCase
from django.utils.translation import gettext_lazy

from django_orjson import default


class DefaultTests(SimpleTestCase):
    def test_timedelta(self):
        assert default(datetime.timedelta(days=1, hours=2)) == "P1DT02H00M00S"

    def test_decimal(self):
        assert default(decimal.Decimal("9.99")) == "9.99"

    def test_promise(self):
        assert default(gettext_lazy("hello")) == "hello"

    def test_unsupported_type(self):
        with pytest.raises(TypeError):
            default(object())

    @pytest.mark.skipif(django.VERSION < (5, 0), reason="Django 5.0+")
    def test_django_json_encoder_source(self):
        """
        Monitor DjangoJSONEncoder for new types that may need handling.
        """
        source = getsource(DjangoJSONEncoder)
        expected = dedent(
            """\
            class DjangoJSONEncoder(json.JSONEncoder):
                \"\"\"
                JSONEncoder subclass that knows how to encode date/time, decimal types, and
                UUIDs.
                \"\"\"

                def default(self, o):
                    # See "Date Time String Format" in the ECMA-262 specification.
                    if isinstance(o, datetime.datetime):
                        r = o.isoformat()
                        if o.microsecond:
                            r = r[:23] + r[26:]
                        if r.endswith("+00:00"):
                            r = r.removesuffix("+00:00") + "Z"
                        return r
                    elif isinstance(o, datetime.date):
                        return o.isoformat()
                    elif isinstance(o, datetime.time):
                        if is_aware(o):
                            raise ValueError("JSON can't represent timezone-aware times.")
                        r = o.isoformat()
                        if o.microsecond:
                            r = r[:12]
                        return r
                    elif isinstance(o, datetime.timedelta):
                        return duration_iso_string(o)
                    elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
                        return str(o)
                    else:
                        return super().default(o)
            """
        )
        assert source == expected
