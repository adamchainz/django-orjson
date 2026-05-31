from __future__ import annotations

import json as _json
from typing import Any

from django.db import models

from django_orjson.db import JSONField

try:
    from django.db.models import JSONNull as _JSONNull

    _json_null_default: type = _JSONNull
except ImportError:
    _json_null_default = dict  # type: ignore[assignment]


class JSONModel(models.Model):
    value = JSONField()

    class Meta:
        app_label = "testapp"


class NullableJSONModel(models.Model):
    value = JSONField(null=True)
    value_custom = JSONField(null=True, blank=True)

    class Meta:
        app_label = "testapp"


class RelatedJSONModel(models.Model):
    value = JSONField()
    json_model = models.ForeignKey(NullableJSONModel, on_delete=models.CASCADE)
    summary = models.TextField(null=True)

    class Meta:
        app_label = "testapp"


class JSONNullDefaultModel(models.Model):
    value = JSONField(default=_json_null_default)

    class Meta:
        app_label = "testapp"


class _CustomSerializationJSONField(JSONField):
    def get_prep_value(self, value: object) -> object:
        if value is not None:
            return _json.dumps(value)
        return value


class CustomSerializationJSONModel(models.Model):
    json_field = _CustomSerializationJSONField()

    class Meta:
        app_label = "testapp"


class Widget(models.Model):
    name: Any = models.CharField(max_length=100)
    price: Any = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at: Any = models.DateTimeField(null=True, blank=True)
    duration: Any = models.DurationField(null=True, blank=True)
