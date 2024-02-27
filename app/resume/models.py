import secrets
import string
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    alphabet = string.ascii_letters + string.digits
    secure_string = ''.join(secrets.choice(alphabet) for _ in range(20))
    newname = f'{secure_string}.{ext}'
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    new_path = f'{BASE_DIR}/media/resumes/{newname}'

    return new_path


class Applicant_Industry(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Resume(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
    industry = models.ForeignKey(Applicant_Industry, null=True, on_delete=models.CASCADE, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    resume = models.FileField(upload_to=rename_file, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.phone
