from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import django
import orjson
from django.core import exceptions
from django.db.models import JSONField as DjangoJSONField

from django_orjson import default

if django.VERSION >= (6, 1):  # pragma: no branch
    from django.db.models import JSONNull  # type: ignore [attr-defined]

    def _json_field_default(obj: Any) -> Any:
        if isinstance(obj, JSONNull):
            return None
        return default(obj)

else:
    _json_field_default = default


class JSONField(DjangoJSONField):
    def __init__(self, *args: Any, option: int | None = None, **kwargs: Any) -> None:
        self._orjson_option = option
        if kwargs.pop("encoder", None):
            raise TypeError(f"encoder is not supported for {self.__class__.__name__}")
        if kwargs.pop("decoder", None):
            raise TypeError(f"decoder is not supported for {self.__class__.__name__}")
        super().__init__(*args, encoder=None, decoder=None, **kwargs)  # type: ignore [misc]

    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        path = "django_orjson.db.JSONField"
        if self._orjson_option is not None:
            kwargs["option"] = self._orjson_option
        return name, path, args, kwargs

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        if value is None:
            return value
        if not isinstance(value, str):
            return value
        try:
            return orjson.loads(value)
        except orjson.JSONDecodeError:
            return value

    def get_db_prep_value(
        self, value: Any, connection: Any, prepared: bool = False
    ) -> Any:
        if not prepared:
            value = self.get_prep_value(value)
        if value is None:
            return value
        return orjson.dumps(
            value, default=_json_field_default, option=self._orjson_option
        ).decode()

    def validate(self, value: Any, model_instance: Any) -> None:
        super(DjangoJSONField, self).validate(value, model_instance)
        try:
            orjson.dumps(value, default=_json_field_default, option=self._orjson_option)
        except TypeError:
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )
