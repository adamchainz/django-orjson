from __future__ import annotations

from typing import Any

import orjson
from django.test import SimpleTestCase as DjangoSimpleTestCase
from django.test.client import JSON_CONTENT_TYPE_RE
from django.test.client import AsyncClient as DjangoAsyncClient
from django.test.client import Client as DjangoClient

from django_orjson import default


class OrjsonMixin:
    def _encode_json(self, data: Any, content_type: str) -> Any:
        should_encode = JSON_CONTENT_TYPE_RE.match(content_type) and isinstance(
            data, (dict, list, tuple)
        )
        return orjson.dumps(data, default=default) if should_encode else data

    def _parse_json(self, response: Any, **extra: Any) -> Any:
        if extra:
            raise TypeError("orjson.loads() does not accept keyword arguments")
        if not hasattr(response, "_json"):
            content_type = response.get("Content-Type")
            if not JSON_CONTENT_TYPE_RE.match(content_type):
                raise ValueError(
                    f'Content-Type header is "{content_type}", not "application/json"'
                )

            response._json = orjson.loads(response.content)
        return response._json


class AsyncClient(OrjsonMixin, DjangoAsyncClient):
    pass


class Client(OrjsonMixin, DjangoClient):
    pass


class SimpleTestCase(DjangoSimpleTestCase):
    client_class = Client
    async_client_class = AsyncClient

    def assertJSONEqual(
        self, raw: str | bytes | bytearray, expected_data: Any, msg: str | None = None
    ) -> None:
        try:
            data = orjson.loads(raw)
        except orjson.JSONDecodeError:
            self.fail(f"First argument is not valid JSON: {raw!r}")
        if isinstance(expected_data, (str, bytes, bytearray)):
            try:
                expected_data = orjson.loads(expected_data)
            except orjson.JSONDecodeError:
                self.fail(f"Second argument is not valid JSON: {expected_data!r}")
        self.assertEqual(data, expected_data, msg=msg)

    def assertJSONNotEqual(
        self, raw: str | bytes | bytearray, expected_data: Any, msg: str | None = None
    ) -> None:
        try:
            data = orjson.loads(raw)
        except orjson.JSONDecodeError:
            self.fail(f"First argument is not valid JSON: {raw!r}")
        if isinstance(expected_data, (str, bytes, bytearray)):
            try:
                expected_data = orjson.loads(expected_data)
            except orjson.JSONDecodeError:
                self.fail(f"Second argument is not valid JSON: {expected_data!r}")
        self.assertNotEqual(data, expected_data, msg=msg)
