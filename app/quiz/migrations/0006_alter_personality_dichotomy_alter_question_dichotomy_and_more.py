# Generated by Django 5.0.3 on 2024-03-12 05:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0005_rename_description_personalitytype_describe"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personality",
            name="dichotomy",
            field=models.CharField(
                choices=[
                    ("I/E", "Introversion/Extroversion"),
                    ("S/N", "Sensing/Intuition"),
                    ("T/F", "Thinking/Feeling"),
                    ("J/P", "Judging/Perceiving"),
                ],
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="dichotomy",
            field=models.CharField(
                choices=[
                    ("I/E", "Introversion/Extroversion"),
                    ("S/N", "Sensing/Intuition"),
                    ("T/F", "Thinking/Feeling"),
                    ("J/P", "Judging/Perceiving"),
                ],
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="userresponse",
            name="dichotomy",
            field=models.CharField(
                choices=[
                    ("I/E", "Introversion/Extroversion"),
                    ("S/N", "Sensing/Intuition"),
                    ("T/F", "Thinking/Feeling"),
                    ("J/P", "Judging/Perceiving"),
                ],
                max_length=3,
            ),
        ),
    ]