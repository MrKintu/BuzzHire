from django.db import models

from resume.models import Resume


class Question(models.Model):
    dichotomy_choices = (
        ('I/E', 'Introversion/Extroversion'),
        ('S/I', 'Sensing/Intuition'),
        ('T/F', 'Thinking/Feeling'),
        ('J/P', 'Judging/Perceiving')
    )

    text = models.TextField()
    dichotomy = models.CharField(max_length=3, choices=dichotomy_choices)

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    user_id = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True)  # Assuming each user has an ID
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    response = models.IntegerField()  # Assuming the response scale is 1-7


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

    type_name = models.CharField(max_length=4, choices=type_choices, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.type_name


class Personality(models.Model):
    dichotomy_choices = (
        ('I/E', 'Introversion/Extroversion'),
        ('S/I', 'Sensing/Intuition'),
        ('T/F', 'Thinking/Feeling'),
        ('J/P', 'Judging/Perceiving')
    )

    name = models.CharField(max_length=20)
    abbrv = models.CharField(max_length=1)
    dichotomy = models.CharField(max_length=3, choices=dichotomy_choices)
    describe = models.TextField()
