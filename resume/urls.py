from django.urls import path

from .views import (edit_resume, job_details, jobs_applied, apply_to_job, education_history, edit_education,
                    past_roles, edit_roles)

urlpatterns = [
    path("edit-resume/", edit_resume, name="edit-resume"),
    path("view-job/<int:pk>/", job_details, name="view-job"),
    path("apply-job/<int:pk>/", apply_to_job, name="apply-job"),
    path("jobs-applied/", jobs_applied, name="jobs-applied"),
    path("education/", education_history, name="education"),
    path("edit-education/<int:pk>/", edit_education, name="edit-education"),
    path("past-roles/", past_roles, name="past-roles"),
    path("edit-roles/<int:pk>/", edit_roles, name="edit-roles"),
]
