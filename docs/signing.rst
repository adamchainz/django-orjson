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
