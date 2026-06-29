from __future__ import annotations

import datetime
import decimal
import inspect
from textwrap import dedent

from django.test import SimpleTestCase
from django.utils import html as django_html
from django.utils.safestring import SafeString

from django_orjson.html import json_script


class JsonScriptTests(SimpleTestCase):
    def test_basic(self):
        result = json_script({"key": "value"})
        assert isinstance(result, SafeString)
        assert result == '<script type="application/json">{"key":"value"}</script>'

    def test_element_id(self):
        result = json_script({"key": "value"}, "data")
        assert result == (
            '<script id="data" type="application/json">{"key":"value"}</script>'
        )

    def test_html_escapes(self):
        result = json_script({"key": "<a> & </a>"})
        assert "<a>" not in result
        assert "</a>" not in result
        assert "&" not in result.replace("</script>", "")
        assert "\\u003C" in result
        assert "\\u003E" in result
        assert "\\u0026" in result

    def test_element_id_escaped(self):
        result = json_script({}, '"><script>')
        assert '"><script>' not in result
        assert "&quot;&gt;&lt;script&gt;" in result

    def test_lazy_string(self):
        from django.utils.translation import gettext_lazy

        result = json_script(gettext_lazy("&<>"), "test_id")
        assert result == (
            '<script id="test_id" type="application/json">'
            '"\\u0026\\u003C\\u003E"</script>'
        )

    def test_lazy_string_nested(self):
        from django.utils.translation import gettext_lazy

        result = json_script(
            {"a": gettext_lazy("<script>test&ing</script>")}, "test_id"
        )
        assert result == (
            '<script id="test_id" type="application/json">'
            '{"a":"\\u003Cscript\\u003Etest\\u0026ing\\u003C/script\\u003E"}'
            "</script>"
        )

    def test_default_decimal(self):
        result = json_script({"value": decimal.Decimal("1.5")})
        assert '"1.5"' in result

    def test_default_timedelta(self):
        result = json_script({"value": datetime.timedelta(seconds=1)})
        assert '"P0DT00H00M01S"' in result

    def test_custom_default(self):
        class Thing:
            pass

        def default(obj):
            if isinstance(obj, Thing):
                return "thing"
            raise TypeError  # pragma: no cover

        result = json_script({"value": Thing()}, default=default)
        assert '"thing"' in result

    def test_option_sort_keys(self):
        import orjson

        result = json_script({"b": 1, "a": 2}, option=orjson.OPT_SORT_KEYS)
        assert result == '<script type="application/json">{"a":2,"b":1}</script>'

    def test_upstream_source(self):
        source = dedent(inspect.getsource(django_html.json_script))
        expected = dedent(
            '''\
            def json_script(value, element_id=None, encoder=None):
                """
                Escape all the HTML/XML special characters with their unicode escapes, so
                value is safe to be output anywhere except for inside a tag attribute. Wrap
                the escaped JSON in a script tag.
                """
                from django.core.serializers.json import DjangoJSONEncoder

                json_str = json.dumps(value, cls=encoder or DjangoJSONEncoder).translate(
                    _json_script_escapes
                )
                if element_id:
                    template = \'<script id="{}" type="application/json">{}</script>\'
                    args = (element_id, mark_safe(json_str))
                else:
                    template = \'<script type="application/json">{}</script>\'
                    args = (mark_safe(json_str),)
                return format_html(template, *args)
            '''
        )
        assert source == expected

    def test_escapes_upstream_source(self):
        assert django_html._json_script_escapes == {  # type: ignore[attr-defined]
            ord(">"): "\\u003E",
            ord("<"): "\\u003C",
            ord("&"): "\\u0026",
        }
