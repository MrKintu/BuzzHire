from django.db import models
from users.models import User

# Create your models here.

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    mentee_capacity = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.user.username}'s Mentor Profile"


class MentorshipConnection(models.Model):
    mentor = models.ForeignKey(User, related_name='mentor_connections', on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, related_name='mentee_connections', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mentor', 'mentee')

    def __str__(self):
        return f"{self.mentor.username} -> {self.mentee.username}"
