from __future__ import annotations

import inspect
from textwrap import dedent

from django.template import Context, Template, defaultfilters
from django.test import SimpleTestCase


class JsonScriptFilterTests(SimpleTestCase):
    def test_basic(self):
        template = Template("{% load django_orjson %}{{ data|json_script }}")
        rendered = template.render(Context({"data": {"key": "value"}}))
        assert rendered == '<script type="application/json">{"key":"value"}</script>'

    def test_element_id(self):
        template = Template("{% load django_orjson %}{{ data|json_script:'data' }}")
        rendered = template.render(Context({"data": {"key": "value"}}))
        assert rendered == (
            '<script id="data" type="application/json">{"key":"value"}</script>'
        )

    def test_complex_escaping(self):
        template = Template("{% load django_orjson %}{{ value|json_script:'test_id' }}")
        rendered = template.render(
            Context({"value": {"a": "testing\r\njson 'string\" <b>escaping</b>"}})
        )
        assert rendered == (
            '<script id="test_id" type="application/json">'
            '{"a":"testing\\r\\njson \'string\\" '
            '\\u003Cb\\u003Eescaping\\u003C/b\\u003E"}'
            "</script>"
        )

    def test_upstream_source(self):
        source = dedent(inspect.getsource(defaultfilters.json_script))
        expected = dedent(
            '''\
            @register.filter(is_safe=True)
            def json_script(value, element_id=None):
                """
                Output value JSON-encoded, wrapped in a <script type="application/json">
                tag (with an optional id).
                """
                return _json_script(value, element_id)
            '''
        )
        assert source == expected
