from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    title_choices = (
        ("Mr", "Mr"),
        ("Mrs", "Mrs"),
        ("Ms", "Ms"),
    )

    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True, choices=title_choices)
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True)
    d_o_b = models.DateField(null=True, blank=True)
    is_recruiter = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    has_resume = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)
