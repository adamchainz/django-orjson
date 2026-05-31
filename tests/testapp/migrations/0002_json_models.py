from __future__ import annotations

import django.db.models.deletion
from django.db import migrations, models

import django_orjson.db


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JSONModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", django_orjson.db.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="NullableJSONModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", django_orjson.db.JSONField(null=True)),
                ("value_custom", django_orjson.db.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="RelatedJSONModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", django_orjson.db.JSONField()),
                ("summary", models.TextField(null=True)),
                (
                    "json_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="testapp.nullablejsonmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JSONNullDefaultModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", django_orjson.db.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name="CustomSerializationJSONModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("json_field", django_orjson.db.JSONField()),
            ],
        ),
    ]
