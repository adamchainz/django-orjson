from __future__ import annotations

import datetime
import decimal
from io import StringIO
from zoneinfo import ZoneInfo

import orjson
import pytest
from django.core.serializers.base import DeserializationError
from django.test import TestCase

from django_orjson.serializers.json import Deserializer as JsonDeserializer
from django_orjson.serializers.json import Serializer as JsonSerializer
from django_orjson.serializers.jsonl import Deserializer as JsonlDeserializer
from django_orjson.serializers.jsonl import Serializer as JsonlSerializer
from tests.testapp.models import Widget


class JsonSerializerTests(TestCase):
    def test_basic_structure(self):
        Widget.objects.create(name="test")
        result = JsonSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result)
        assert len(data) == 1
        assert data[0]["model"] == "testapp.widget"
        assert "pk" in data[0]
        assert data[0]["fields"]["name"] == "test"

    def test_multiple_objects(self):
        Widget.objects.create(name="a")
        Widget.objects.create(name="b")
        result = JsonSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result)
        assert len(data) == 2

    def test_decimal_field(self):
        Widget.objects.create(name="test", price=decimal.Decimal("9.99"))
        result = JsonSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result)
        assert data[0]["fields"]["price"] == "9.99"

    def test_datetime_field(self):
        dt = datetime.datetime(2024, 1, 15, 12, 30, 0, tzinfo=ZoneInfo("UTC"))
        Widget.objects.create(name="test", created_at=dt)
        result = JsonSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result)
        assert data[0]["fields"]["created_at"].startswith("2024-01-15T12:30:00")

    def test_duration_field(self):
        Widget.objects.create(name="test", duration=datetime.timedelta(days=1, hours=2))
        result = JsonSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result)
        assert data[0]["fields"]["duration"] == "1 02:00:00"

    def test_null_fields(self):
        Widget.objects.create(name="test", price=None, created_at=None, duration=None)
        result = JsonSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result)
        assert data[0]["fields"]["price"] is None
        assert data[0]["fields"]["created_at"] is None
        assert data[0]["fields"]["duration"] is None

    def test_indent(self):
        w = Widget.objects.create(name="test")
        result = JsonSerializer().serialize(Widget.objects.all(), indent=2)
        assert (
            result
            == f'[\n{{\n  "model": "testapp.widget",\n  "pk": {w.pk},\n  "fields": {{\n    "name": "test",\n    "price": null,\n    "created_at": null,\n    "duration": null\n  }}\n}}\n]\n'
        )
        orjson.loads(result)

    def test_indent_multiple_objects(self):
        Widget.objects.create(name="a")
        Widget.objects.create(name="b")
        result = JsonSerializer().serialize(Widget.objects.all(), indent=2)
        assert "\n" in result
        data = orjson.loads(result)
        assert len(data) == 2

    def test_output_to_stream(self):
        Widget.objects.create(name="test")
        stream = StringIO()
        JsonSerializer().serialize(Widget.objects.all(), stream=stream)
        data = orjson.loads(stream.getvalue())
        assert len(data) == 1

    def test_selected_fields(self):
        Widget.objects.create(name="test", price=decimal.Decimal("1.00"))
        result = JsonSerializer().serialize(Widget.objects.all(), fields=["name"])
        data = orjson.loads(result)
        assert "name" in data[0]["fields"]
        assert "price" not in data[0]["fields"]


class JsonDeserializerTests(TestCase):
    def test_basic(self):
        Widget.objects.create(name="original")
        serialized = JsonSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonDeserializer(serialized))
        assert len(objs) == 1
        objs[0].save()
        assert Widget.objects.get().name == "original"

    def test_roundtrip_decimal(self):
        Widget.objects.create(name="test", price=decimal.Decimal("12.34"))
        serialized = JsonSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonDeserializer(serialized))
        objs[0].save()
        assert Widget.objects.get().price == decimal.Decimal("12.34")

    def test_roundtrip_datetime(self):
        dt = datetime.datetime(2024, 6, 1, 9, 0, 0, tzinfo=ZoneInfo("UTC"))
        Widget.objects.create(name="test", created_at=dt)
        serialized = JsonSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonDeserializer(serialized))
        objs[0].save()
        assert Widget.objects.get().created_at == dt

    def test_roundtrip_duration(self):
        d = datetime.timedelta(days=2, hours=3, minutes=15)
        Widget.objects.create(name="test", duration=d)
        serialized = JsonSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonDeserializer(serialized))
        objs[0].save()
        assert Widget.objects.get().duration == d

    def test_bytes_input(self):
        Widget.objects.create(name="test")
        serialized = JsonSerializer().serialize(Widget.objects.all())
        objs = list(JsonDeserializer(serialized.encode()))
        assert len(objs) == 1

    def test_stream_input(self):
        Widget.objects.create(name="test")
        serialized = JsonSerializer().serialize(Widget.objects.all())
        objs = list(JsonDeserializer(StringIO(serialized)))
        assert len(objs) == 1

    def test_invalid_json_raises(self):
        with pytest.raises(DeserializationError):
            list(JsonDeserializer("not valid json"))

    def test_invalid_model_raises(self):
        data = '[{"model": "testapp.nonexistent", "pk": 1, "fields": {}}]'
        with pytest.raises(DeserializationError):
            list(JsonDeserializer(data))


class JsonlSerializerTests(TestCase):
    def test_basic_structure(self):
        Widget.objects.create(name="test")
        result = JsonlSerializer().serialize(Widget.objects.all())
        lines = [line for line in result.splitlines() if line]
        assert len(lines) == 1
        data = orjson.loads(lines[0])
        assert data["model"] == "testapp.widget"
        assert data["fields"]["name"] == "test"

    def test_multiple_objects(self):
        Widget.objects.create(name="a")
        Widget.objects.create(name="b")
        result = JsonlSerializer().serialize(Widget.objects.all())
        lines = [line for line in result.splitlines() if line]
        assert len(lines) == 2
        assert orjson.loads(lines[0])["fields"]["name"] in ("a", "b")
        assert orjson.loads(lines[1])["fields"]["name"] in ("a", "b")

    def test_decimal_field(self):
        Widget.objects.create(name="test", price=decimal.Decimal("9.99"))
        result = JsonlSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result.splitlines()[0])
        assert data["fields"]["price"] == "9.99"

    def test_datetime_field(self):
        dt = datetime.datetime(2024, 1, 15, 12, 30, 0, tzinfo=ZoneInfo("UTC"))
        Widget.objects.create(name="test", created_at=dt)
        result = JsonlSerializer().serialize(Widget.objects.all())
        data = orjson.loads(result.splitlines()[0])
        assert data["fields"]["created_at"].startswith("2024-01-15T12:30:00")

    def test_no_indent(self):
        Widget.objects.create(name="test")
        result = JsonlSerializer().serialize(Widget.objects.all(), indent=2)
        # JSONL ignores indent; each object is compact on one line
        lines = [line for line in result.splitlines() if line]
        assert len(lines) == 1

    def test_output_to_stream(self):
        Widget.objects.create(name="test")
        stream = StringIO()
        JsonlSerializer().serialize(Widget.objects.all(), stream=stream)
        lines = [line for line in stream.getvalue().splitlines() if line]
        assert len(lines) == 1


class JsonlDeserializerTests(TestCase):
    def test_basic(self):
        Widget.objects.create(name="original")
        serialized = JsonlSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonlDeserializer(serialized))
        assert len(objs) == 1
        objs[0].save()
        assert Widget.objects.get().name == "original"

    def test_roundtrip_decimal(self):
        Widget.objects.create(name="test", price=decimal.Decimal("12.34"))
        serialized = JsonlSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonlDeserializer(serialized))
        objs[0].save()
        assert Widget.objects.get().price == decimal.Decimal("12.34")

    def test_roundtrip_datetime(self):
        dt = datetime.datetime(2024, 6, 1, 9, 0, 0, tzinfo=ZoneInfo("UTC"))
        Widget.objects.create(name="test", created_at=dt)
        serialized = JsonlSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonlDeserializer(serialized))
        objs[0].save()
        assert Widget.objects.get().created_at == dt

    def test_roundtrip_duration(self):
        d = datetime.timedelta(days=2, hours=3, minutes=15)
        Widget.objects.create(name="test", duration=d)
        serialized = JsonlSerializer().serialize(Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(JsonlDeserializer(serialized))
        objs[0].save()
        assert Widget.objects.get().duration == d

    def test_bytes_input(self):
        Widget.objects.create(name="test")
        serialized = JsonlSerializer().serialize(Widget.objects.all())
        objs = list(JsonlDeserializer(serialized.encode()))
        assert len(objs) == 1

    def test_stream_input(self):
        Widget.objects.create(name="test")
        serialized = JsonlSerializer().serialize(Widget.objects.all())
        objs = list(JsonlDeserializer(StringIO(serialized)))
        assert len(objs) == 1

    def test_blank_lines_ignored(self):
        Widget.objects.create(name="test")
        serialized = JsonlSerializer().serialize(Widget.objects.all())
        objs = list(JsonlDeserializer("\n" + serialized + "\n"))
        assert len(objs) == 1

    def test_invalid_json_raises(self):
        with pytest.raises(DeserializationError):
            list(JsonlDeserializer("not valid json\n"))

    def test_invalid_model_raises(self):
        data = '{"model": "testapp.nonexistent", "pk": 1, "fields": {}}\n'
        with pytest.raises(DeserializationError):
            list(JsonlDeserializer(data))


class SerializationModulesTests(TestCase):
    def test_json_serialize(self):
        from django.core import serializers

        Widget.objects.create(name="test")
        result = serializers.serialize("json", Widget.objects.all())
        data = orjson.loads(result)
        assert data[0]["fields"]["name"] == "test"

    def test_json_deserialize(self):
        from django.core import serializers

        Widget.objects.create(name="test")
        serialized = serializers.serialize("json", Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(serializers.deserialize("json", serialized))
        assert len(objs) == 1

    def test_jsonl_serialize(self):
        from django.core import serializers

        Widget.objects.create(name="test")
        result = serializers.serialize("jsonl", Widget.objects.all())
        data = orjson.loads(result.splitlines()[0])
        assert data["fields"]["name"] == "test"

    def test_jsonl_deserialize(self):
        from django.core import serializers

        Widget.objects.create(name="test")
        serialized = serializers.serialize("jsonl", Widget.objects.all())
        Widget.objects.all().delete()
        objs = list(serializers.deserialize("jsonl", serialized))
        assert len(objs) == 1
