import string
import random
from pathlib import Path
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    rand_strings = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                           for i in range(5))
    newname = '{}{}.{}'.format(rand_strings, uuid4().hex, ext)
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    new_path = f'{BASE_DIR}\\media\\{newname}'

    return new_path


class Resume(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    industry = models.CharField(max_length=100, null=True, blank=True)
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
