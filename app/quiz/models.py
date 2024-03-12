from django.contrib.auth.models import User
from django.db import models


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

    text = models.CharField(max_length=100)
    dichotomy = models.CharField(max_length=3, choices=dichotomy_choices)

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    dichotomy_choices = (
        ('I/E', 'Introversion/Extroversion'),
        ('S/N', 'Sensing/Intuition'),
        ('T/F', 'Thinking/Feeling'),
        ('J/P', 'Judging/Perceiving')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    response = models.IntegerField()
    dichotomy = models.CharField(max_length=3, choices=dichotomy_choices)


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

    combo = models.CharField(max_length=4, choices=type_choices, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    describe = models.TextField()

    def __str__(self):
        return self.name
