from django.urls import path
from .views import edit_company, all_applicants, single_applicant


urlpatterns = [
    path("edit-company/", edit_company, name="edit-company"),
    path("results/<int:pk>/", all_applicants, name="results"),
    path("view-applicant/<int:pk>/", single_applicant, name="view-applicant"),
]
