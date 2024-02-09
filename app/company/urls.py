from django.urls import path
from .views import edit_company


urlpatterns = [
    path("edit-company/", edit_company, name="edit-company")
]
