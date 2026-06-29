Testing
=======

.. currentmodule:: django_orjson.test

.. class:: Client

   A subclass of Django’s test client that uses orjson to:

   1. Encode request JSON.
   2. Parse response JSON, in the patched-on |response.json()|__ method.

   .. |response.json()| replace:: ``response.json()``
   __ https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Response.json

   Request encoding uses :func:`django_orjson.default` for extended type support.
   Django’s ``json_encoder`` argument is not used.

   Normally, you’ll want to use it by subclassing django-orjson’s :class:`SimpleTestCase` (below), which sets the client class automatically.
   But you can also use it directly in your own test classes by setting |client_class|__.

   .. |client_class| replace:: ``client_class``
   __ https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.client_class

   If you use pytest fixtures, you can replace the |client fixture|__ from pytest-django with a custom one that returns django-orjson’s client in your ``conftest.py``:

   .. |client fixture| replace:: the ``client`` fixture
   __ https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client

   .. code-block:: python

       # conftest.py
       import pytest
       from django_orjson.test import Client


       @pytest.fixture
       def client():
           return Client()

.. class:: AsyncClient

   A subclass of Django’s async test client, with the same extensions as the above sync client, :class:`Client`.

.. class:: SimpleTestCase

   A subclass of Django’s |SimpleTestCase|__ that:

   1. Uses :class:`Client` as its ``client_class``.
   2. Uses :class:`AsyncClient` as its ``async_client_class``.
   3. Parses JSON with orjson in |assertJSONEqual()|__ and |assertJSONNotEqual()|__.

   .. |SimpleTestCase| replace:: ``SimpleTestCase``
   __ https://docs.djangoproject.com/en/stable/topics/testing/tools/#simpletestcase

   .. |assertJSONEqual()| replace:: ``assertJSONEqual()``
   __ https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertJSONEqual

   .. |assertJSONNotEqual()| replace:: ``assertJSONNotEqual()``
   __ https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertJSONNotEqual

   Use it like Django’s built-in test case:

   .. code-block:: python

       from django_orjson.test import SimpleTestCase


       class MyTests(SimpleTestCase):
           def test_json(self):
               self.assertJSONEqual('{"key":"value"}', {"key": "value"})

   Use it as a base class for your own base test case classes like so:

   .. code-block:: python

       # example/test.py
       from django import test
       from django_orjson.test import SimpleTestCase as OrJsonSimpleTestCase


       class SimpleTestCase(OrJsonSimpleTestCase):
           pass


       class TestCase(SimpleTestCase, test.TestCase):
           pass


       class TransactionTestCase(SimpleTestCase, test.TransactionTestCase):
           pass

   …then your tests can all import from your own base classes instead of Django’s built-in ones, and they’ll get the benefits of django-orjson automatically, like:

   .. code-block:: python

       from example.test import SimpleTestCase


       class IndexTests(SimpleTestCase):
           def test_index(self):
               response = self.client.get("/", headers={"accept": "application/json"})
               assert response.status_code == 200
               assert response.json() == {  # uses orjson to parse the response body
                   "title": "Hello, world!"
               }
