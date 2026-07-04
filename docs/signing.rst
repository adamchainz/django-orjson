Signing
=======

.. module:: django_orjson.signing

.. autoclass:: OrjsonSerializer

   An orjson-based serializer for use with |django.core.signing|__.

   .. |django.core.signing| replace:: ``django.core.signing``
   __ https://docs.djangoproject.com/en/stable/topics/signing/

   Pass it as the ``serializer`` argument to |signing.dumps()|__ and |signing.loads()|__, or the `lower-level methods <https://docs.djangoproject.com/en/6.0/topics/signing/#signing-complex-data>`__ ``Signer.sign_object()`` and ``Signer.unsign_object()``:

   .. |signing.dumps()| replace:: ``signing.dumps()``
   __ https://docs.djangoproject.com/en/stable/topics/signing/#django.core.signing.dumps

   .. |signing.loads()| replace:: ``signing.loads()``
   __ https://docs.djangoproject.com/en/stable/topics/signing/#django.core.signing.loads

   .. code-block:: python

       from django.core import signing

       from django_orjson.signing import OrjsonSerializer

       token = signing.dumps({"user_id": 1}, serializer=OrjsonSerializer)
       data = signing.loads(token, serializer=OrjsonSerializer)

   .. warning:: **One-way migration**

      Migrating from Django’s ``JSONSerializer`` to ``OrjsonSerializer`` is safe, but the reverse case is not.

      Tokens signed with ``JSONSerializer`` can be verified and read by ``OrjsonSerializer`` without issue.
      But tokens signed with ``OrjsonSerializer`` can be silently misread by ``JSONSerializer``.

      Django’s ``JSONSerializer.loads`` decodes the payload as latin-1 before parsing, while ``OrjsonSerializer`` writes non-ASCII characters as raw UTF-8.
      If you switch back, any token payload containing non-ASCII data will be *silently* misread as mojibake.
      For example, ``héllo`` will become ``hÃ©llo``, with no ``BadSignature`` or ``UnicodeDecodeError`` raised.
