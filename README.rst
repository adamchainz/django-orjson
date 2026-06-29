=============
django-orjson
=============

.. image:: https://img.shields.io/github/actions/workflow/status/adamchainz/django-orjson/main.yml.svg?branch=main&style=for-the-badge
   :target: https://github.com/adamchainz/django-orjson/actions?workflow=CI

.. image:: https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge
  :target: https://github.com/adamchainz/django-orjson/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/django-orjson.svg?style=for-the-badge
   :target: https://pypi.org/project/django-orjson/

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

`orjson <https://github.com/ijl/orjson>`__-powered utilities for Django.

----

**Work smarter and faster** with my book `Boost Your Django DX <https://adamchainz.gumroad.com/l/byddx>`__ which covers many ways to improve your development experience.

----

Requirements
------------

Python 3.10 to 3.14 supported.

Django 5.2 to 6.1 supported.

Installation
------------

1. Install with **pip**:

   .. code-block:: sh

       python -m pip install django-orjson

2. Add to your ``INSTALLED_APPS``:

   .. code-block:: python

       INSTALLED_APPS = [
           ...,
           "django_orjson",
       ]

Reference
---------

``django_orjson.default``
^^^^^^^^^^^^^^^^^^^^^^^^^

A function for use with |orjson’s default parameter|__ that extends orjson to support serializing these extra types:

.. |orjson’s default parameter| replace:: orjson’s ``default`` parameter
__ https://github.com/ijl/orjson#default

* |decimal.Decimal|__

  .. |decimal.Decimal| replace:: ``decimal.Decimal``
  __ https://docs.python.org/3/library/decimal.html#decimal.Decimal

* |datetime.timedelta|__

  .. |datetime.timedelta| replace:: ``datetime.timedelta``
  __ https://docs.python.org/3/library/datetime.html#datetime.timedelta

* Django’s ``Promise`` objects, as used for `lazy translations <https://docs.djangoproject.com/en/6.0/topics/i18n/translation/#lazy-translations>`__

This function is similar to Django’s |DjangoJSONEncoder|__, used with the standard library ``json`` module.

.. |DjangoJSONEncoder| replace:: ``DjangoJSONEncoder``
__ https://docs.djangoproject.com/en/stable/topics/serialization/#djangojsonencoder

``django_orjson.http.JsonResponse``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A subclass of Django's |HttpResponse|__ that serializes its content with |orjson.dumps()|__ instead of the standard library's ``json.dumps()``.
This provides faster serialization and native support for additional types such as ``datetime``, ``UUID``, and ``dataclasses``.

.. |HttpResponse| replace:: ``HttpResponse``
__ https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponse

.. |orjson.dumps()| replace:: ``orjson.dumps()``
__ https://github.com/ijl/orjson?tab=readme-ov-file#serialize

Usage mirrors Django's built-in |JsonResponse|__:

.. |JsonResponse| replace:: ``JsonResponse``
__ https://docs.djangoproject.com/en/stable/ref/request-response/#jsonresponse-objects

.. code-block:: python

    from django_orjson.http import JsonResponse


    def my_view(request):
        return JsonResponse({"key": "value"})

``data``
~~~~~~~~

The object to serialize.

``default``
~~~~~~~~~~~

Passes through to |orjson’s default parameter2|__.
Defaults to ``django_orjson.default``, for extended type support.

.. |orjson’s default parameter2| replace:: orjson’s ``default`` parameter
__ https://github.com/ijl/orjson#default

Pass a different callable to handle additional types, or chain to ``django_orjson.default`` for the built-in behaviour:

.. code-block:: python

    import pathlib

    from django_orjson import default as base_default


    def default(obj):
        if isinstance(obj, pathlib.Path):
            return str(obj)
        return base_default(obj)


    JsonResponse({"path": pathlib.Path("/tmp/file.txt")}, default=default)

``option``
~~~~~~~~~~

An optional integer of orjson option flags.
See the `orjson documentation <https://github.com/ijl/orjson?tab=readme-ov-file#option>`__ for available options.
Multiple options can be combined with ``|``:

.. code-block:: python

    import orjson

    JsonResponse({"b": 1, "a": 2}, option=orjson.OPT_SORT_KEYS)

``django_orjson.html.json_script``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An orjson-powered version of Django's |json_script|__ utility.
It serializes ``value`` with ``orjson.dumps()``, escapes HTML/XML special characters, and wraps the result in a ``<script type="application/json">`` tag.

.. |json_script| replace:: ``json_script()``
__ https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.json_script

.. code-block:: python

    from django_orjson.html import json_script

    json_script({"key": "value"}, "data")

Arguments:

* ``value``: the object to serialize.
* ``element_id`` (optional): an ``id`` attribute for the ``<script>`` tag.
* ``default`` (optional): passes through to orjson; defaults to ``django_orjson.default``.
* ``option`` (optional): passes through to orjson.

``json_script`` template filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A template filter equivalent to Django's built-in |json_script_filter|__, using the function above.
In your templates:

.. |json_script_filter| replace:: ``json_script``
__ https://docs.djangoproject.com/en/stable/ref/templates/builtins/#json-script

.. code-block:: html+django

    {% load django_orjson %}
    {{ data|json_script:"my-data" }}

``django_orjson.serializers``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

orjson-powered copies of Django's built-in JSON serializers, for use with |dumpdata|__ and |loaddata|__.
They will also be used automatically for ``json``/``jsonl`` format fixtures in |TransactionTestCase.fixtures|__ and |the testserver command|__.

.. |dumpdata| replace:: ``dumpdata``
__ https://docs.djangoproject.com/en/stable/ref/django-admin/#dumpdata

.. |loaddata| replace:: ``loaddata``
__ https://docs.djangoproject.com/en/stable/ref/django-admin/#loaddata

.. |TransactionTestCase.fixtures| replace:: ``TransactionTestCase.fixtures``
__ https://docs.djangoproject.com/en/stable/topics/testing/tools/#fixture-loading

.. |the testserver command| replace:: the ``testserver`` command
__ https://docs.djangoproject.com/en/stable/ref/django-admin/#testserver

Register the serializers by adding entries to |SERIALIZATION_MODULES|__ in your settings:

.. |SERIALIZATION_MODULES| replace:: ``SERIALIZATION_MODULES``
__ https://docs.djangoproject.com/en/stable/ref/settings/#serialization-modules

.. code-block:: python

    SERIALIZATION_MODULES = {
        "json": "django_orjson.serializers.json",
        "jsonl": "django_orjson.serializers.jsonl",
    }

Then use them like the built-in serializers:

.. code-block:: console

    $ python manage.py dumpdata --format json myapp > data.json
    $ python manage.py loaddata --format json data.json

    $ python manage.py dumpdata --format jsonl myapp > data.jsonl
    $ python manage.py loaddata --format jsonl data.jsonl

Or programmatically:

.. code-block:: python

    from django.core import serializers

    data = serializers.serialize("json", queryset)
    for obj in serializers.deserialize("json", data):
        obj.save()

The serializers’ output is compatible with Django's standard JSON deserializer, except that when ``indent`` is passed, the output uses orjson's two-space indentation regardless of the value specified.

``django_orjson.test.Client``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A subclass of Django's test client that uses orjson to:

1. Encode request JSON.
2. Parse response JSON, in the patched-on |response.json()|__ method.

.. |response.json()| replace:: ``response.json()``
__ https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.Response.json

Request encoding uses ``django_orjson.default`` for extended type support.
Django's ``json_encoder`` argument is not used.

Normally, you’ll want to use it by subclassing django-orjson’s ``SimpleTestCase`` (below), which sets the client class automatically.
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

``django_orjson.test.AsyncClient``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A subclass of Django’s async test client, with the same extensions as the above sync client, ``django_orjson.test.Client``.

``django_orjson.test.SimpleTestCase``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A subclass of Django's |SimpleTestCase|__ that:

1. Uses ``django_orjson.test.Client`` as its ``client_class``.
2. Uses ``django_orjson.test.AsyncClient`` as its ``async_client_class``.
3. Parses JSON with orjson in |assertJSONEqual()|__ and |assertJSONNotEqual()|__.

.. |SimpleTestCase| replace:: ``SimpleTestCase``
__ https://docs.djangoproject.com/en/stable/topics/testing/tools/#simpletestcase

.. |assertJSONEqual()| replace:: ``assertJSONEqual()``
__ https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertJSONEqual

.. |assertJSONNotEqual()| replace:: ``assertJSONNotEqual()``
__ https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertJSONNotEqual

Use it like Django's built-in test case:

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

…then your tests can all import from your own base classes instead of Django's built-in ones, and they’ll get the benefits of django-orjson automatically, like:

.. code-block:: python

    from example.test import SimpleTestCase


    class IndexTests(SimpleTestCase):
        def test_index(self):
            response = self.client.get("/", headers={"accept": "application/json"})
            assert response.status_code == 200
            assert response.json() == {  # uses orjson to parse the response body
                "title": "Hello, world!"
            }
