# Generated by Django 5.0.3 on 2024-03-11 03:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0002_alter_question_text"),
    ]

    operations = [
        migrations.RenameField(
            model_name="personalitytype",
            old_name="type_name",
            new_name="combo",
        ),
        migrations.AddField(
            model_name="personalitytype",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="personality",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]