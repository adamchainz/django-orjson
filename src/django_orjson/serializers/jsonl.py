from __future__ import annotations

from collections.abc import Generator
from typing import Any

import orjson
from django.core.serializers.base import DeserializationError
from django.core.serializers.jsonl import Deserializer as JSONLDeserializer
from django.core.serializers.jsonl import Serializer as JSONLSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer

from django_orjson import default


class Serializer(JSONLSerializer):
    def _init_options(self) -> None:
        self._current = None

    def end_object(self, obj: Any) -> None:
        self.stream.write(
            orjson.dumps(self.get_dump_object(obj), default=default).decode()
        )
        self.stream.write("\n")
        self._current = None


class Deserializer(JSONLDeserializer):
    # Copy-paste-modified from upstream: JSONLDeserializer.__init__ hardcodes a
    # call to its own _get_lines(), so we must skip it and call PythonDeserializer
    # directly to substitute our orjson-based _get_lines().
    def __init__(self, stream_or_string: Any, **options: Any) -> None:
        if isinstance(stream_or_string, bytes):
            stream_or_string = stream_or_string.decode()
        if isinstance(stream_or_string, str):
            stream_or_string = stream_or_string.splitlines()
        PythonDeserializer.__init__(self, self._get_lines(stream_or_string), **options)

    @staticmethod
    def _get_lines(
        stream: Any,
    ) -> Generator[Any, None, None]:
        for line in stream:
            if not line.strip():
                continue
            try:
                yield orjson.loads(line)
            except Exception as exc:
                raise DeserializationError(str(exc)) from exc
