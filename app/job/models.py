import secrets
import string
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models

from company.models import Company
from resume.models import Resume
from users.models import UserInfo


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    alphabet = string.ascii_letters + string.digits
    secure_string = ''.join(secrets.choice(alphabet) for _ in range(20))
    newname = f'{secure_string}.{ext}'
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    new_path = f'{BASE_DIR}/media/jobs/{newname}'

    return new_path


class JobPost(models.Model):
    type_choices = (
        ("Remote", "Remote"),
        ("Onsite", "Onsite"),
        ("Hybrid", "Hybrid"),
    )

    industry_choices = (
        ("Transportation", "Transportation"),
        ("Pharmaceutical", "Pharmaceutical"),
        ("Telecommunications", "Telecommunications"),
        ("Manufacturing", "Manufacturing"),
        ("Mining", "Mining"),
        ("Hospitality", "Hospitality"),
        ("Media and News", "Media and News"),
        ("Agriculture", "Agriculture"),
        ("Computer and Technology", "Computer and Technology"),
        ("Education", "Education"),
        ("Finance and Economics", "Finance and Economics"),
        ("Health Care", "Health Care")
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=type_choices, null=True, blank=True)
    industry = models.CharField(max_length=100, blank=True, null=True, choices=industry_choices)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pay = models.PositiveIntegerField(null=True, blank=True)
    describe = models.TextField()
    tasks = models.TextField()
    ideal_candidate = models.TextField()
    available = models.BooleanField(default=True)
    download = models.FileField(upload_to=rename_file, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title


class ApplyJob(models.Model):
    status_choices = (
        ("Approved", "Approved"),
        ("Declined", "Declined"),
        ("Pending", "Pending"),
    )

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, null=True, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices)
    reference = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.reference
