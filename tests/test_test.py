from __future__ import annotations

import datetime
import inspect
from textwrap import dedent

import pytest
from django.test import SimpleTestCase as DjangoSimpleTestCase
from django.test.client import AsyncClient as DjangoAsyncClient
from django.test.client import Client as DjangoClient

from django_orjson.http import JsonResponse
from django_orjson.test import AsyncClient, Client, SimpleTestCase


class ClientTests(DjangoSimpleTestCase):
    async_client_class = AsyncClient
    client_class = Client

    async def test_async_client_encode_json(self):
        assert (
            self.async_client._encode_json(  # type: ignore[attr-defined]
                {"key": "value"}, "application/json"
            )
            == b'{"key":"value"}'
        )

    async def test_async_client_parse_json(self):
        response = JsonResponse({"key": "value"})

        assert self.async_client._parse_json(response) == {  # type: ignore[attr-defined]
            "key": "value"
        }

    def test_async_client_upstream_base_classes(self):
        assert (
            DjangoAsyncClient._encode_json  # type: ignore[attr-defined]
            is DjangoClient._encode_json  # type: ignore[attr-defined]
        )
        assert DjangoAsyncClient._parse_json is DjangoClient._parse_json  # type: ignore[attr-defined]

    def test_encode_json(self):
        assert (
            self.client._encode_json(  # type: ignore[attr-defined]
                {"key": "value"}, "application/json"
            )
            == b'{"key":"value"}'
        )

    def test_encode_json_uses_django_orjson_default(self):
        assert (
            self.client._encode_json(  # type: ignore[attr-defined]
                {"duration": datetime.timedelta(days=1, hours=2)}, "application/json"
            )
            == b'{"duration":"P1DT02H00M00S"}'
        )

    def test_encode_json_non_json_content_type(self):
        data = {"key": "value"}

        assert self.client._encode_json(data, "text/plain") is data  # type: ignore[attr-defined]

    def test_encode_json_non_container(self):
        data = b'{"key":"value"}'

        assert self.client._encode_json(data, "application/json") is data  # type: ignore[attr-defined]

    def test_encode_json_upstream_source(self):
        source = dedent(inspect.getsource(DjangoClient._encode_json))  # type: ignore[attr-defined]
        expected = dedent(
            '''\
            def _encode_json(self, data, content_type):
                """
                Return encoded JSON if data is a dict, list, or tuple and content_type
                is application/json.
                """
                should_encode = JSON_CONTENT_TYPE_RE.match(content_type) and isinstance(
                    data, (dict, list, tuple)
                )
                return json.dumps(data, cls=self.json_encoder) if should_encode else data
            '''
        )
        assert source == expected

    def test_parse_json(self):
        response = JsonResponse({"key": "value"})

        assert self.client._parse_json(response) == {  # type: ignore[attr-defined]
            "key": "value"
        }

    def test_parse_json_caches_result(self):
        response = JsonResponse({"key": "value"})

        assert (
            self.client._parse_json(response)  # type: ignore[attr-defined]
            is self.client._parse_json(response)  # type: ignore[attr-defined]
        )

    def test_parse_json_content_type_error(self):
        response = JsonResponse({"key": "value"}, content_type="text/plain")

        with pytest.raises(ValueError) as excinfo:
            self.client._parse_json(response)  # type: ignore[attr-defined]

        assert str(excinfo.value) == (
            'Content-Type header is "text/plain", not "application/json"'
        )

    def test_parse_json_extra_error(self):
        response = JsonResponse({"key": "value"})

        with pytest.raises(TypeError) as excinfo:
            self.client._parse_json(response, parse_float=float)  # type: ignore[attr-defined]

        assert str(excinfo.value) == "orjson.loads() does not accept keyword arguments"

    def test_parse_json_upstream_source(self):
        source = dedent(inspect.getsource(DjangoClient._parse_json))  # type: ignore[attr-defined]
        expected = dedent(
            """\
            def _parse_json(self, response, **extra):
                if not hasattr(response, "_json"):
                    if not JSON_CONTENT_TYPE_RE.match(response.get("Content-Type")):
                        raise ValueError(
                            'Content-Type header is "%s", not "application/json"'
                            % response.get("Content-Type")
                        )
                    response._json = json.loads(response.text, **extra)
                return response._json
            """
        )
        assert source == expected


class SimpleTestCaseTests(SimpleTestCase):
    def test_client_class(self):
        assert self.client_class is Client
        assert self.async_client_class is AsyncClient

    def test_assert_json_equal(self):
        self.assertJSONEqual(b'{"key":"value"}', {"key": "value"})
        self.assertJSONEqual('{"key":"value"}', '{"key":"value"}')

    def test_assert_json_equal_first_argument_error(self):
        with pytest.raises(AssertionError) as excinfo:
            self.assertJSONEqual("invalid", {})

        assert str(excinfo.value) == "First argument is not valid JSON: 'invalid'"

    def test_assert_json_equal_second_argument_error(self):
        with pytest.raises(AssertionError) as excinfo:
            self.assertJSONEqual("{}", "invalid")

        assert str(excinfo.value) == "Second argument is not valid JSON: 'invalid'"

    def test_assert_json_equal_upstream_source(self):
        source = dedent(inspect.getsource(DjangoSimpleTestCase.assertJSONEqual))
        expected = dedent(
            '''\
            def assertJSONEqual(self, raw, expected_data, msg=None):
                """
                Assert that the JSON fragments raw and expected_data are equal.
                Usual JSON non-significant whitespace rules apply as the heavyweight
                is delegated to the json library.
                """
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    self.fail("First argument is not valid JSON: %r" % raw)
                if isinstance(expected_data, str):
                    try:
                        expected_data = json.loads(expected_data)
                    except ValueError:
                        self.fail("Second argument is not valid JSON: %r" % expected_data)
                self.assertEqual(data, expected_data, msg=msg)
            '''
        )
        assert source == expected

    def test_assert_json_not_equal(self):
        self.assertJSONNotEqual(b'{"key":"value"}', {"key": "other"})
        self.assertJSONNotEqual('{"key":"value"}', '{"key":"other"}')

    def test_assert_json_not_equal_first_argument_error(self):
        with pytest.raises(AssertionError) as excinfo:
            self.assertJSONNotEqual("invalid", {})

        assert str(excinfo.value) == "First argument is not valid JSON: 'invalid'"

    def test_assert_json_not_equal_second_argument_error(self):
        with pytest.raises(AssertionError) as excinfo:
            self.assertJSONNotEqual("{}", "invalid")

        assert str(excinfo.value) == "Second argument is not valid JSON: 'invalid'"

    def test_assert_json_not_equal_upstream_source(self):
        source = dedent(inspect.getsource(DjangoSimpleTestCase.assertJSONNotEqual))
        expected = dedent(
            '''\
            def assertJSONNotEqual(self, raw, expected_data, msg=None):
                """
                Assert that the JSON fragments raw and expected_data are not equal.
                Usual JSON non-significant whitespace rules apply as the heavyweight
                is delegated to the json library.
                """
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    self.fail("First argument is not valid JSON: %r" % raw)
                if isinstance(expected_data, str):
                    try:
                        expected_data = json.loads(expected_data)
                    except json.JSONDecodeError:
                        self.fail("Second argument is not valid JSON: %r" % expected_data)
                self.assertNotEqual(data, expected_data, msg=msg)
            '''
        )
        assert source == expected
