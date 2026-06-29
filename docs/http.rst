HTTP responses
==============

.. currentmodule:: django_orjson.http

.. autoclass:: JsonResponse

   A subclass of Django’s |HttpResponse|__ that serializes its content with |orjson.dumps()|__ instead of the standard library’s ``json.dumps()``.
   This provides faster serialization and native support for additional types such as ``datetime``, ``UUID``, and ``dataclasses``.

   .. |HttpResponse| replace:: ``HttpResponse``
   __ https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponse

   .. |orjson.dumps()| replace:: ``orjson.dumps()``
   __ https://github.com/ijl/orjson?tab=readme-ov-file#serialize

   Usage mirrors Django’s built-in |JsonResponse|__:

   .. |JsonResponse| replace:: ``JsonResponse``
   __ https://docs.djangoproject.com/en/stable/ref/request-response/#jsonresponse-objects

   .. code-block:: python

       from django_orjson.http import JsonResponse


       def my_view(request):
           return JsonResponse({"key": "value"})

   :param data:
      The object to serialize.

   :param default:
      Passes through to |orjson’s default parameter|__.
      Defaults to :func:`django_orjson.default`, for extended type support.

      .. |orjson’s default parameter| replace:: orjson’s ``default`` parameter
      __ https://github.com/ijl/orjson#default

      Pass a different callable to handle additional types, or chain to :func:`django_orjson.default` for the built-in behaviour:

      .. code-block:: python

          import pathlib

          from django_orjson import default as base_default


          def default(obj):
              if isinstance(obj, pathlib.Path):
                  return str(obj)
              return base_default(obj)


          JsonResponse({"path": pathlib.Path("/tmp/file.txt")}, default=default)

   :param option:
      An optional integer of orjson option flags.
      See the `orjson documentation <https://github.com/ijl/orjson?tab=readme-ov-file#option>`__ for available options.
      Multiple options can be combined with ``|``:

      .. code-block:: python

          import orjson

          JsonResponse({"b": 1, "a": 2}, option=orjson.OPT_SORT_KEYS)

   :param kwargs:
      Other ``HttpResponse`` parameters.
