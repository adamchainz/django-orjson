Sessions
========

.. module:: django_orjson.sessions

.. autoclass:: OrjsonSerializer

   An orjson-based session serializer, replacing Django's built-in |JSONSerializer|__.

   .. |JSONSerializer| replace:: ``JSONSerializer``
   __ https://docs.djangoproject.com/en/stable/topics/http/sessions/#session-serialization

   Configure it in your settings:

   .. code-block:: python

       SESSION_SERIALIZER = "django_orjson.sessions.OrjsonSerializer"

   .. warning:: **One-way migration**

      Migrating from Django’s ``JSONSerializer`` to ``OrjsonSerializer`` is safe, but the reverse case is not.

      Sessions written by ``JSONSerializer`` can be read by ``OrjsonSerializer`` without issue.
      But sessions written by ``OrjsonSerializer`` can be silently misread by ``JSONSerializer``.

      See the note in :doc:`signing` for more information—Django’s session ``JSONSerializer`` is a re-export of the signing one, so they share this limitation.
