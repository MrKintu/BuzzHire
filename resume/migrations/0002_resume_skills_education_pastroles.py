# Generated by Django 5.0.3 on 2024-04-03 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resume", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="skills",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Education",
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
                ("degree", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "institution",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("start_year", models.DateField()),
                ("end_year", models.DateField()),
                ("gpa", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "resume",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resume.resume",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PastRoles",
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
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("company", models.CharField(blank=True, max_length=100, null=True)),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("responsibilities", models.TextField()),
                (
                    "resume",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resume.resume",
                    ),
                ),
            ],
        ),
    ]
