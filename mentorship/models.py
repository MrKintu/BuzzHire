from django.db import models
from users.models import User

# Create your models here.

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    mentee_capacity = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.user.username}'s Mentor Profile"
