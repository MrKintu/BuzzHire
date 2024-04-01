from django.urls import path
from .views import index, applicant_dash, recruiter_dash, search


urlpatterns = [
    path("", index, name="index"),
    path("applicant-dash/", applicant_dash, name="applicant-dash"),
    path("recruiter-dash/", recruiter_dash, name="recruiter-dash"),
    path("search/<str:query>/", search, name="search"),
]
