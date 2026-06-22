from __future__ import annotations

from typing import Any

import orjson
from django.core.serializers.base import DeserializationError
from django.core.serializers.json import Deserializer as JSONDeserializer
from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer

from django_orjson import default


class Serializer(JSONSerializer):
    _orjson_option: int | None

    def _init_options(self) -> None:
        super()._init_options()  # type: ignore [misc]
        self._orjson_option = (
            orjson.OPT_INDENT_2 if self.options.get("indent") else None
        )

    def end_object(self, obj: Any) -> None:
        if not self.first:
            self.stream.write(",")
            if not self._orjson_option:
                self.stream.write(" ")
        if self._orjson_option:
            self.stream.write("\n")
        self.stream.write(
            orjson.dumps(
                self.get_dump_object(obj),
                default=default,
                option=self._orjson_option,
            ).decode()
        )
        self._current = None


class Deserializer(JSONDeserializer):
    def __init__(self, stream_or_string: Any, **options: Any) -> None:
        if not isinstance(stream_or_string, (bytes, str)):
            stream_or_string = stream_or_string.read()
        try:
            objects = orjson.loads(stream_or_string)
        except Exception as exc:
            raise DeserializationError(str(exc)) from exc
        PythonDeserializer.__init__(self, objects, **options)
