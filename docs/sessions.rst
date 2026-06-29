Sessions
========

.. module:: django_orjson.sessions

.. autoclass:: OrjsonSerializer

   An orjson-based session serializer, replacing Django's built-in |JSONSerializer|__.

   .. |JSONSerializer| replace:: ``JSONSerializer``
   __ https://docs.djangoproject.com/en/stable/topics/http/sessions/#session-serialization

   Since both this serializer and Django's built-in ``JSONSerializer`` produce standard JSON, switching between them is safe — existing sessions remain readable after the change.

   Configure it in your settings:

   .. code-block:: python

       SESSION_SERIALIZER = "django_orjson.sessions.OrjsonSerializer"
