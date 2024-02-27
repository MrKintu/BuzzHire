# Generated by Django 5.0.2 on 2024-02-25 07:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0004_remove_applyjob_user_applyjob_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applyjob",
            name="status",
            field=models.CharField(
                choices=[
                    ("Approved", "Approved"),
                    ("Declined", "Declined"),
                    ("Pending", "Pending"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
    ]
