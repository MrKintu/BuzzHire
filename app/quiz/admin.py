from django.contrib import admin

from .models import Personality, Question, UserResponse, PersonalityType

admin.site.register(Personality)
admin.site.register(Question)
admin.site.register(UserResponse)
admin.site.register(PersonalityType)
