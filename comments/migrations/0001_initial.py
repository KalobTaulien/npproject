# Generated by Django 5.0.6 on 2024-06-10 18:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("date_posted", models.DateTimeField(auto_now_add=True)),
                ("anonymous_content", models.BooleanField(default=False)),
                (
                    "agreement",
                    models.IntegerField(
                        choices=[
                            (4, "Strongly agree"),
                            (2, "Yes, but with reservations"),
                            (0, "It's complicated"),
                            (-2, "No, with reservations"),
                            (-4, "Strongly no"),
                        ],
                        default=0,
                    ),
                ),
                ("text", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Reply",
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
                ("date_posted", models.DateTimeField(auto_now_add=True)),
                ("anonymous_content", models.BooleanField(default=False)),
                (
                    "agreement",
                    models.IntegerField(
                        choices=[
                            (4, "Strongly agree"),
                            (2, "Yes, but with reservations"),
                            (0, "It's complicated"),
                            (-2, "No, with reservations"),
                            (-4, "Strongly no"),
                        ],
                        default=0,
                    ),
                ),
                ("text", models.TextField()),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="comments.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
