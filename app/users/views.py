from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .form import RegisterUserForm
from resume.models import Resume


# Register Applicant
def new_applicant(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_applicant = True
            var.save()
            Resume.object.create(user=var)
            messages.info(request, "Your account has been created.")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong...")
            return redirect("new-applicant")
    else:
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, 'users/new-applicant.html', context)


# Register Recruiter
def new_recruiter(request):
    pass
