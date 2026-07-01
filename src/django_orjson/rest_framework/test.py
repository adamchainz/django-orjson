from __future__ import annotations

from rest_framework.test import APIClient as BaseAPIClient
from rest_framework.test import APILiveServerTestCase as BaseAPILiveServerTestCase
from rest_framework.test import APISimpleTestCase as BaseAPISimpleTestCase
from rest_framework.test import APITestCase as BaseAPITestCase
from rest_framework.test import APITransactionTestCase as BaseAPITransactionTestCase

from django_orjson.test import Client, SimpleTestCase


class APIClient(Client, BaseAPIClient):  # type: ignore[misc]
    pass


class APISimpleTestCase(SimpleTestCase, BaseAPISimpleTestCase):  # type: ignore[misc]
    client_class = APIClient


class APITransactionTestCase(SimpleTestCase, BaseAPITransactionTestCase):  # type: ignore[misc]
    client_class = APIClient


class APITestCase(SimpleTestCase, BaseAPITestCase):  # type: ignore[misc]
    client_class = APIClient


class APILiveServerTestCase(SimpleTestCase, BaseAPILiveServerTestCase):  # type: ignore[misc]
    client_class = APIClient
