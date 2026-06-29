from __future__ import annotations

from typing import Any

SECRET_KEY = "NOTASECRET"

ALLOWED_HOSTS: list[str] = []

DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "testdb",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django_orjson",
    "tests.testapp",
]

MIDDLEWARE: list[str] = []

SERIALIZATION_MODULES = {
    "json": "django_orjson.serializers.json",
    "jsonl": "django_orjson.serializers.jsonl",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

USE_TZ = True
