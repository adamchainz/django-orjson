from __future__ import annotations

from typing import Any

from django.db import models


class Widget(models.Model):
    name: Any = models.CharField(max_length=100)
    price: Any = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at: Any = models.DateTimeField(null=True, blank=True)
    duration: Any = models.DurationField(null=True, blank=True)
