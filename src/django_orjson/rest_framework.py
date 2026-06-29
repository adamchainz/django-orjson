from __future__ import annotations

from collections.abc import Callable
from typing import Any

import orjson
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser as BaseJSONParser
from rest_framework.renderers import JSONRenderer as BaseJSONRenderer

from django_orjson import default as django_orjson_default


class JSONRenderer(BaseJSONRenderer):  # type: ignore[misc]
    default: Callable[[Any], Any] = staticmethod(django_orjson_default)
    option: int = 0

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict[str, Any] | None = None,
    ) -> bytes:
        if data is None:
            return b""

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        option = self.option
        if indent is not None:
            option |= orjson.OPT_INDENT_2

        ret: bytes = orjson.dumps(data, default=self.default, option=option)
        return ret


class JSONParser(BaseJSONParser):  # type: ignore[misc]
    renderer_class = JSONRenderer

    def parse(
        self,
        stream: Any,
        media_type: str | None = None,
        parser_context: dict[str, Any] | None = None,
    ) -> Any:
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)
        data = stream.read()

        if isinstance(data, bytes) and encoding.lower().replace("_", "-") not in (
            "utf-8",
            "utf8",
        ):
            data = data.decode(encoding)

        try:
            return orjson.loads(data)
        except ValueError as exc:
            raise ParseError(f"JSON parse error - {exc}") from exc
