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

Django 4.2 to 6.0 supported.

Installation
------------

1. Install with **pip**:

   .. code-block:: sh

       python -m pip install django-orjson

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
