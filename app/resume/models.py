import os
import secrets
import string
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models

from quiz.models import PersonalityType


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    alphabet = string.ascii_letters + string.digits
    secure_string = ''.join(secrets.choice(alphabet) for _ in range(20))
    newname = f'{secure_string}.{ext}'
    BASE_DIR = Path(__file__).resolve().parent.parent
    new_path = f'{BASE_DIR}/media/resumes/{newname}'

    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # root_directory = current_directory
    # while not os.path.exists(os.path.join(root_directory, 'manage.py')):
    #     root_directory = os.path.dirname(root_directory)
    # new_path = f"{root_directory}\\media\\resumes\\{newname}"

    return new_path


class Resume(models.Model):
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True, choices=industry_choices)
    profession = models.CharField(max_length=100, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    resume = models.FileField(upload_to=rename_file, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    personality = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.phone


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    start_year = models.DateField()
    end_year = models.DateField()
    gpa = models.CharField(max_length=10, null=True, blank=True)


class PastRoles(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    responsibilities = models.TextField()
