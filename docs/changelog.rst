=========
Changelog
=========

* Switch package build backend from setuptools to `uv_build <https://docs.astral.sh/uv/concepts/build-backend/>`__.
  This makes builds with uv about nine times faster, since uv runs the backend natively, without creating a build environment or spawning a Python process.
  Additionally, source distributions no longer include test files, which setuptools previously included incompletely, missing the files needed to actually run them.

1.1.0 (2026-07-01)
------------------

* Added Django REST Framework testing tools in :mod:`django_orjson.rest_framework.test`.

  `PR #14 <https://github.com/adamchainz/django-orjson/pull/14>`__.

1.0.0 (2026-06-30)
------------------

* Initial release.
