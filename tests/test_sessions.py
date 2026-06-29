from __future__ import annotations

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
        from django.contrib.sessions.serializers import JSONSerializer

        data = {"_auth_user_id": "42", "key": "value"}
        encoded = JSONSerializer().dumps(data)
        assert OrjsonSerializer().loads(encoded) == data

    def test_orjson_encoded_decoded_by_django_json(self):
        from django.contrib.sessions.serializers import JSONSerializer

        data = {"_auth_user_id": "42", "key": "value"}
        encoded = OrjsonSerializer().dumps(data)
        assert JSONSerializer().loads(encoded) == data


class SessionBackendIntegrationTests(TestCase):
    @override_settings(
        SESSION_SERIALIZER="django_orjson.sessions.OrjsonSerializer",
        SESSION_ENGINE="django.contrib.sessions.backends.signed_cookies",
        SECRET_KEY="test-secret-key",
    )
    def test_session_encode_decode_roundtrip(self):
        from django.contrib.sessions.backends.signed_cookies import SessionStore

        store = SessionStore()
        store["user_id"] = 42
        store["username"] = "alice"
        encoded = store.encode(dict(store))
        decoded = store.decode(encoded)
        assert decoded["user_id"] == 42
        assert decoded["username"] == "alice"
