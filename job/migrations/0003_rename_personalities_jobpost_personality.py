# Generated by Django 5.0.3 on 2024-04-04 20:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0002_jobpost_personalities_jobpost_skills_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="jobpost",
            old_name="personalities",
            new_name="personality",
        ),
    ]
