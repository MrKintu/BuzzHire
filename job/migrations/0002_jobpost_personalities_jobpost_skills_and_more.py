# Generated by Django 5.0.3 on 2024-04-04 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0001_initial"),
        ("job", "0001_initial"),
        ("quiz", "0003_alter_userpersonality_graph"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobpost",
            name="personalities",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="quiz.personality",
            ),
        ),
        migrations.AddField(
            model_name="jobpost",
            name="skills",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="jobpost",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="company.company",
            ),
        ),
        migrations.AlterField(
            model_name="jobpost",
            name="describe",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="jobpost",
            name="ideal_candidate",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="jobpost",
            name="tasks",
            field=models.TextField(blank=True, null=True),
        ),
    ]
