import secrets
import string
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models

from company.models import Company


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    alphabet = string.ascii_letters + string.digits
    secure_string = ''.join(secrets.choice(alphabet) for _ in range(20))
    newname = f'{secure_string}.{ext}'
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    new_path = f'{BASE_DIR}/media/jobs/{newname}'

    return new_path


class Job_Industry(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class JobPost(models.Model):
    type_choices = (
        ("Remote", "Remote"),
        ("Onsite", "Onsite"),
        ("Hybrid", "Hybrid"),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    industry = models.ForeignKey(Job_Industry, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pay = models.PositiveIntegerField(default=14)
    describe = models.TextField()
    tasks = models.TextField()
    ideal = models.TextField()
    available = models.BooleanField(default=False)
    download = models.FileField(upload_to=rename_file, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    job_type = models.CharField(max_length=20, choices=type_choices, null=True, blank=True)

    def __str__(self):
        return self.title


class ApplyJob(models.Model):
    status_choices = (
        ("Approved", "Approved"),
        ("Declined", "Declined"),
        ("Pending", "Pending"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices)
