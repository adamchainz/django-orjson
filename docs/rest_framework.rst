Django REST framework
=====================

.. module:: django_orjson.rest_framework

Extensions for using orjson with |Django REST framework|__.

.. |Django REST framework| replace:: Django REST framework
__ https://www.django-rest-framework.org/

When using these, install django-orjson with its ``drf`` extra to ensure Django REST framework compatibility, for example:

.. code-block:: console

    $ python -m pip install 'django-orjson[drf]'

Then configure Django REST framework to swap the default JSON renderer and parser with the orjson-based ones, for example:

.. code-block:: python

    REST_FRAMEWORK = {
        "DEFAULT_RENDERER_CLASSES": [
            "django_orjson.rest_framework.JSONRenderer",
        ],
        "DEFAULT_PARSER_CLASSES": [
            "django_orjson.rest_framework.JSONParser",
        ],
    }

.. autoclass:: JSONRenderer

   A subclass of |JSONRenderer|__ that serializes response data with ``orjson.dumps()``.

   .. |JSONRenderer| replace:: ``rest_framework.renderers.JSONRenderer``
   __ https://www.django-rest-framework.org/api-guide/renderers/#jsonrenderer

   The renderer uses orjson’s native serialization path where possible, with :func:`django_orjson.default` configured as orjson’s ``default`` callable for extra Django type support such as ``decimal.Decimal`` and ``datetime.timedelta``.
   When indentation is requested, it uses orjson’s two-space indentation regardless of the requested indentation width.

   Customize orjson’s ``default`` and ``option`` parameters by subclassing:

   .. code-block:: python

       import pathlib

       import orjson
       from django_orjson import default as base_default
       from django_orjson.rest_framework import JSONRenderer


       class MyJSONRenderer(JSONRenderer):
           option = orjson.OPT_UTC_Z

           @staticmethod
           def default(obj):
               if isinstance(obj, pathlib.Path):
                   return str(obj)
               return base_default(obj)

.. autoclass:: JSONParser

   A subclass of |JSONParser|__ that parses request data with ``orjson.loads()``.

   .. |JSONParser| replace:: ``rest_framework.parsers.JSONParser``
   __ https://www.django-rest-framework.org/api-guide/parsers/#jsonparser

Testing
-------

.. module:: django_orjson.rest_framework.test

The following test case classes mirror |DRF’s test case classes|__, with django-orjson’s :class:`APIClient` as ``client_class`` and django-orjson’s JSON assertion methods:

.. |DRF’s test case classes| replace:: DRF’s test case classes
__ https://www.django-rest-framework.org/api-guide/testing/#api-test-cases

.. autoclass:: APISimpleTestCase

.. autoclass:: APITransactionTestCase

.. autoclass:: APITestCase

.. autoclass:: APILiveServerTestCase

Use them like DRF’s built-in classes:

.. code-block:: python

    from django_orjson.rest_framework.test import APITestCase


    class MyAPITests(APITestCase):
        def test_create_account(self):
            response = self.client.post(
                "/accounts/",
                {"name": "DabApps"},
                format="json",
            )
            assert response.status_code == 201

.. autoclass:: APIClient

   A subclass of both :class:`django_orjson.test.Client` and |APIClient|__.

   .. |APIClient| replace:: ``rest_framework.test.APIClient``
   __ https://www.django-rest-framework.org/api-guide/testing/#apiclient
