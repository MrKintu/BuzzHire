from django.shortcuts import render, redirect
from job.models import JobPost
from company.models import Company


def index(request):
    if request.method == "POST":
        data = request.POST
        query = data["search"]
    else:
        return render(request, "dashboard/index.html")


def applicant_dash(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "dashboard/applicant-dash.html")


def recruiter_dash(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "dashboard/recruiter-dash.html")
