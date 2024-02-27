from django.urls import path
from .views import edit_resume, job_details, apply_to_job, jobs_applied


urlpatterns = [
    path("edit-resume/", edit_resume, name="edit-resume"),
    path("view-job/<int:pk>/", job_details, name="view-job"),
    path("apply-job/<int:pk>/", apply_to_job, name="apply-job"),
    path("jobs-applied/", jobs_applied, name="jobs-applied"),
]
