from __future__ import annotations

from typing import Any

import orjson

from django_orjson import default as _default


class OrjsonSerializer:
    def dumps(self, obj: Any) -> bytes:
        value: bytes = orjson.dumps(obj, default=_default)
        return value

    def loads(self, data: bytes) -> Any:
        return orjson.loads(data)
