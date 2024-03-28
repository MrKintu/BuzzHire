from django.contrib.auth.models import User
from django.db import models

from users.models import UserInfo


class Personality(models.Model):
    dichotomy_choices = (
        ('I/E', 'Introversion/Extroversion'),
        ('S/N', 'Sensing/Intuition'),
        ('T/F', 'Thinking/Feeling'),
        ('J/P', 'Judging/Perceiving')
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    abbrv = models.CharField(max_length=1)
    dichotomy = models.CharField(max_length=3, choices=dichotomy_choices)
    describe = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    dichotomy_choices = (
        ('I/E', 'Introversion/Extroversion'),
        ('S/N', 'Sensing/Intuition'),
        ('T/F', 'Thinking/Feeling'),
        ('J/P', 'Judging/Perceiving')
    )

    count = models.IntegerField()
    dichotomy = models.CharField(max_length=50, choices=dichotomy_choices)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    response = models.IntegerField()


class PersonalityType(models.Model):
    type_choices = (
        ('INTJ', 'INTJ'),
        ('INTP', 'INTP'),
        ('ENTJ', 'ENTJ'),
        ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'),
        ('INFP', 'INFP'),
        ('ENFJ', 'ENFJ'),
        ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'),
        ('ISFJ', 'ISFJ'),
        ('ESTJ', 'ESTJ'),
        ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'),
        ('ISFP', 'ISFP'),
        ('ESTP', 'ESTP'),
        ('ESFP', 'ESFP')
    )

    combo = models.CharField(max_length=4, choices=type_choices)
    name = models.CharField(max_length=50, null=True, blank=True)
    describe = models.TextField()

    def __str__(self):
        return self.name


class UserPersonality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    persona = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, null=True, blank=True)
    introversion = models.FloatField()
    extroversion = models.FloatField()
    sensing = models.FloatField()
    intuition = models.FloatField()
    thinking = models.FloatField()
    feeling = models.FloatField()
    judging = models.FloatField()
    perceiving = models.FloatField()
