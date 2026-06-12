from __future__ import annotations

import datetime
import decimal
from typing import Any

from django.utils.duration import duration_iso_string
from django.utils.functional import Promise


def default(obj: Any) -> Any:
    if isinstance(obj, datetime.timedelta):
        return duration_iso_string(obj)
    if isinstance(obj, (decimal.Decimal, Promise)):
        return str(obj)
    raise TypeError
