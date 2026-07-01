from __future__ import annotations

import datetime
import decimal
from io import BytesIO
from zoneinfo import ZoneInfo

import orjson
import pytest
from django.test import SimpleTestCase
from rest_framework.exceptions import ParseError

from django_orjson.rest_framework import JSONParser, JSONRenderer


class JSONRendererTests(SimpleTestCase):
    def test_basic(self):
        result = JSONRenderer().render({"key": "value"})
        assert result == b'{"key":"value"}'
        assert orjson.loads(result) == {"key": "value"}

    def test_none(self):
        assert JSONRenderer().render(None) == b""

    def test_indent_from_media_type(self):
        result = JSONRenderer().render(
            {"key": ["value"]}, accepted_media_type="application/json; indent=4"
        )
        assert result == b'{\n  "key": [\n    "value"\n  ]\n}'

    def test_indent_from_context(self):
        result = JSONRenderer().render({"key": "value"}, renderer_context={"indent": 2})
        assert result == b'{\n  "key": "value"\n}'

    def test_datetime_utc_native(self):
        result = JSONRenderer().render(
            {"value": datetime.datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))}
        )
        assert orjson.loads(result) == {"value": "2024-01-01T00:00:00+00:00"}

    def test_option(self):
        class UTCZJSONRenderer(JSONRenderer):
            option = orjson.OPT_UTC_Z

        result = UTCZJSONRenderer().render(
            {"value": datetime.datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))}
        )
        assert orjson.loads(result) == {"value": "2024-01-01T00:00:00Z"}

    def test_decimal(self):
        result = JSONRenderer().render({"value": decimal.Decimal("1.5")})
        assert orjson.loads(result) == {"value": "1.5"}

    def test_timedelta(self):
        result = JSONRenderer().render({"value": datetime.timedelta(seconds=1)})
        assert orjson.loads(result) == {"value": "P0DT00H00M01S"}


class JSONParserTests(SimpleTestCase):
    def test_basic(self):
        result = JSONParser().parse(BytesIO(b'{"key":"value"}'))
        assert result == {"key": "value"}

    def test_non_utf8_encoding(self):
        data = '{"key":"£"}'.encode("utf-16")
        result = JSONParser().parse(
            BytesIO(data), parser_context={"encoding": "utf-16"}
        )
        assert result == {"key": "£"}

    def test_invalid_json_raises_parse_error(self):
        with pytest.raises(ParseError, match="JSON parse error"):
            JSONParser().parse(BytesIO(b"not valid json"))
