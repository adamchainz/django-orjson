from __future__ import annotations

import django.core.signing as signing
from django.test import TestCase

from django_orjson.signing import OrjsonSerializer


class OrjsonSerializerDirectTests(TestCase):
    def test_dumps_returns_bytes(self):
        result = OrjsonSerializer().dumps({"key": "value"})
        assert isinstance(result, bytes)

    def test_roundtrip_dict(self):
        data = {"key": "value", "num": 42, "list": [1, 2, 3]}
        s = OrjsonSerializer()
        assert s.loads(s.dumps(data)) == data

    def test_roundtrip_nested(self):
        data = {"nested": {"a": 1, "b": [True, False, None]}}
        s = OrjsonSerializer()
        assert s.loads(s.dumps(data)) == data

    def test_roundtrip_list(self):
        data = [1, "two", 3.0, None]
        s = OrjsonSerializer()
        assert s.loads(s.dumps(data)) == data


class SigningDumpsLoadsTests(TestCase):
    def test_roundtrip(self):
        data = {"user_id": 1, "action": "confirm"}
        token = signing.dumps(data, serializer=OrjsonSerializer)
        assert signing.loads(token, serializer=OrjsonSerializer) == data

    def test_roundtrip_list(self):
        data = [1, 2, 3]
        token = signing.dumps(data, serializer=OrjsonSerializer)
        assert signing.loads(token, serializer=OrjsonSerializer) == data

    def test_token_is_string(self):
        token = signing.dumps({"x": 1}, serializer=OrjsonSerializer)
        assert isinstance(token, str)

    def test_tampered_token_raises(self):
        token = signing.dumps({"x": 1}, serializer=OrjsonSerializer)
        import pytest

        with pytest.raises(signing.BadSignature):
            signing.loads(token + "x", serializer=OrjsonSerializer)


class TimestampSignerTests(TestCase):
    def test_sign_unsign_object(self):
        signer = signing.TimestampSigner()
        data = {"key": "value", "num": 42}
        signed = signer.sign_object(data, serializer=OrjsonSerializer)
        assert signer.unsign_object(signed, serializer=OrjsonSerializer) == data

    def test_max_age_not_expired(self):
        signer = signing.TimestampSigner()
        data = {"action": "verify"}
        signed = signer.sign_object(data, serializer=OrjsonSerializer)
        result = signer.unsign_object(signed, serializer=OrjsonSerializer, max_age=60)
        assert result == data
