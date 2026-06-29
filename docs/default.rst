Default function
================

.. currentmodule:: django_orjson

.. function:: default(obj)

   A function for use with |orjson’s default parameter|__ that extends orjson to support serializing these extra types:

   .. |orjson’s default parameter| replace:: orjson’s ``default`` parameter
   __ https://github.com/ijl/orjson#default

   * |decimal.Decimal|__

     .. |decimal.Decimal| replace:: ``decimal.Decimal``
     __ https://docs.python.org/3/library/decimal.html#decimal.Decimal

   * |datetime.timedelta|__

     .. |datetime.timedelta| replace:: ``datetime.timedelta``
     __ https://docs.python.org/3/library/datetime.html#datetime.timedelta

   * Django’s ``Promise`` objects, as used for `lazy translations <https://docs.djangoproject.com/en/stable/topics/i18n/translation/#lazy-translations>`__

   This function is analogous to Django’s |DjangoJSONEncoder|__, which extends the standard library ``json`` module support to the above types.
   You won’t typically need to use this function directly, as it is used internally by the other utilities in this package.

   .. |DjangoJSONEncoder| replace:: ``DjangoJSONEncoder``
   __ https://docs.djangoproject.com/en/stable/topics/serialization/#djangojsonencoder
