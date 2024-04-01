from django.contrib import admin

from .models import Personality, Question, UserResponse, PersonalityType, UserPersonality

admin.site.register(Personality)
admin.site.register(Question)
admin.site.register(UserResponse)
admin.site.register(PersonalityType)
admin.site.register(UserPersonality)
