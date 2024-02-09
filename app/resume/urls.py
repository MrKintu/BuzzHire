from django.urls import path
from .views import edit_resume


urlpatterns = [
    path("edit-resume/", edit_resume, name="edit-resume")
]
