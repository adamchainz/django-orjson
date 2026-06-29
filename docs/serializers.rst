Serializers
===========

.. module:: django_orjson.serializers

orjson-powered copies of Django’s built-in JSON serializers, for use with |dumpdata|__ and |loaddata|__.
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

The serializers’ output is compatible with Django’s standard JSON deserializer, except that when ``indent`` is passed, the output uses orjson’s two-space indentation regardless of the value specified.
