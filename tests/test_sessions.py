from __future__ import annotations

import pytest
from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.contrib.sessions.serializers import JSONSerializer
from django.test import TestCase, override_settings

from django_orjson.sessions import OrjsonSerializer


class OrjsonSerializerTests(TestCase):
    def test_dumps_returns_bytes(self):
        result = OrjsonSerializer().dumps({"key": "value"})
        assert isinstance(result, bytes)

    def test_roundtrip(self):
        data = {"_auth_user_id": "42", "key": "value", "list": [1, 2, 3]}
        s = OrjsonSerializer()
        assert s.loads(s.dumps(data)) == data

    def test_roundtrip_nested(self):
        data = {"nested": {"a": 1, "b": [True, False, None]}}
        s = OrjsonSerializer()
        assert s.loads(s.dumps(data)) == data


class SerializerCompatibilityTests(TestCase):
    def test_django_json_encoded_decoded_by_orjson(self):
        data = {"_auth_user_id": "42", "key": "value"}
        encoded = JSONSerializer().dumps(data)
        assert OrjsonSerializer().loads(encoded) == data

    def test_orjson_encoded_decoded_by_django_json(self):
        data = {"_auth_user_id": "42", "key": "value"}
        encoded = OrjsonSerializer().dumps(data)
        assert JSONSerializer().loads(encoded) == data

    def test_django_json_encoded_decoded_by_orjson_non_ascii(self):
        data = {"username": "héllo", "city": "東京"}
        encoded = JSONSerializer().dumps(data)
        assert OrjsonSerializer().loads(encoded) == data

    @pytest.mark.xfail
    def test_orjson_encoded_decoded_by_django_json_non_ascii(self):
        """
        Sessions written by OrjsonSerializer are silently corrupted when read
        back by Django's JSONSerializer, which decodes the payload as latin-1
        before parsing.
        """
        data = {"username": "héllo", "city": "東京"}
        encoded = OrjsonSerializer().dumps(data)
        decoded = JSONSerializer().loads(encoded)
        assert decoded == data, (
            f"Session written by OrjsonSerializer was read back by Django's"
            f" JSONSerializer as {decoded!r}, silently corrupting non-ASCII"
            f" strings via latin-1 decode of UTF-8 bytes."
        )


class SessionBackendIntegrationTests(TestCase):
    @override_settings(
        SESSION_SERIALIZER="django_orjson.sessions.OrjsonSerializer",
        SESSION_ENGINE="django.contrib.sessions.backends.signed_cookies",
        SECRET_KEY="test-secret-key",
    )
    def test_session_encode_decode_roundtrip(self):
        store = SessionStore()
        store["user_id"] = 42
        store["username"] = "alice"
        encoded = store.encode(dict(store))
        decoded = store.decode(encoded)
        assert decoded["user_id"] == 42
        assert decoded["username"] == "alice"
