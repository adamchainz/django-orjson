HTML utilities
==============

.. currentmodule:: django_orjson.html

.. autofunction:: json_script

   An orjson-powered version of Django’s |json_script|__ utility.
   It serializes ``value`` with ``orjson.dumps()``, escapes HTML/XML special characters, and wraps the result in a ``<script type="application/json">`` tag.

   .. |json_script| replace:: ``json_script()``
   __ https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.json_script

   .. code-block:: python

       from django_orjson.html import json_script

       json_script({"key": "value"}, "data")

   :param value:
      The object to serialize.

   :param element_id:
      An optional ``id`` attribute for the ``<script>`` tag.

   :param default:
      Passes through to orjson; defaults to :func:`django_orjson.default`.

   :param option:
      Passes through to orjson.

``json_script`` template filter
-------------------------------

A template filter equivalent to Django’s built-in |json_script_filter|__, using the function above.
In your templates:

.. |json_script_filter| replace:: ``json_script``
__ https://docs.djangoproject.com/en/stable/ref/templates/builtins/#json-script

.. code-block:: html+django

    {% load django_orjson %}
    {{ data|json_script:"my-data" }}
