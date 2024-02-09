from django.shortcuts import render, redirect


def index(request):
    return render(request, "dashboard/index.html")


def applicant_dash(request):
    return render(request, "dashboard/applicant-dash.html")


def recruiter_dash(request):
    return render(request, "dashboard/recruiter-dash.html")
