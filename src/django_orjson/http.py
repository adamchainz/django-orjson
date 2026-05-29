from __future__ import annotations

from collections.abc import Callable
from typing import Any

import orjson
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json.
    :param default: A callable that gets called for objects that can’t
      otherwise be serialized. It should return a JSON encodable version of the
      object or raise a TypeError.
    :param option: A bitfield of orjson options.
    """

    def __init__(
        self,
        data: Any,
        default: Callable[[Any], Any] | None = None,
        option: int | None = None,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("content_type", "application/json")
        content = orjson.dumps(data, default=default, option=option)
        super().__init__(content=content, **kwargs)
