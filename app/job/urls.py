from django.urls import path
from .views import create_job, update_job, view_jobs, close_job, open_job


urlpatterns = [
    path("", view_jobs, name="view-jobs"),
    path("new-job/", create_job, name="new-job"),
    path("edit-job/<int:pk>", update_job, name="edit-job"),
    path("close-job/<int:pk>", close_job, name="close-job"),
    path("open-job/<int:pk>", open_job, name="open-job"),
]
