from django.urls import path
from .views import new_applicant, new_recruiter, login_user, logout_user

urlpatterns = [
    path("new-applicant/", new_applicant, name="new-applicant"),
    path("new-recruiter/", new_recruiter, name="new-recruiter"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout")
]
