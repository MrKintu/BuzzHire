import random
import string
from pathlib import Path
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from company.models import Company
from resume.models import Resume


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    rand_strings = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                           for i in range(5))
    newname = '{}{}.{}'.format(rand_strings, uuid4().hex, ext)
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    new_path = f'{BASE_DIR}\\media\\jobs\\{newname}'

    return new_path


class JobPost(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    resume = models.ManyToManyField(Resume)
    title = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100)
    pay = models.PositiveIntegerField(default=14)
    describe = models.TextField()
    tasks = models.TextField()
    ideal = models.TextField()
    available = models.BooleanField(default=False)
    download = models.FileField(upload_to=rename_file, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
