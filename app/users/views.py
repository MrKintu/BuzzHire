from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from users.models import UserInfo
from .forms import ApplicantForm, ResumeForm, UserInfoForm, CompanyForm


# Register Applicant
def new_applicant(request):
    if request.method == "POST":
        user_form = ApplicantForm(request.POST)
        resume_form = ResumeForm(request.POST, request.FILES)
        user_info_form = UserInfoForm(request.POST)

        if user_form.is_valid() and resume_form.is_valid() and user_info_form.is_valid():
            user = user_form.save(commit=False)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.is_applicant = True
            user_info.has_resume = True
            user_info.save()

            resume = resume_form.save(commit=False)
            resume.user = user
            resume.save()

            messages.success(request, "Your account has successfully been created.")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong, please try again.")
            # If there are errors, render the form with the error messages
            context = {
                'user_form': user_form,
                'resume_form': resume_form,
                'user_info_form': user_info_form
            }
            return render(request, "users/new-applicant.html", context)
    else:
        user_form = ApplicantForm()
        resume_form = ResumeForm()
        user_info_form = UserInfoForm()
        context = {
            'user_form': user_form,
            'resume_form': resume_form,
            'user_info_form': user_info_form
        }
        return render(request, "users/new-applicant.html", context)


# Register Recruiter
def new_recruiter(request):
    if request.method == "POST":
        user_form = ApplicantForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        company_form = CompanyForm(request.POST)

        if user_form.is_valid() and user_info_form.is_valid() and company_form.is_valid():
            user = user_form.save(commit=False)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.is_recruiter = True
            user_info.has_company = True
            user_info.save()

            company = company_form.save(commit=False)
            company.user = user
            company.save()

            messages.success(request, "Your account has successfully been created.")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong, please try again.")
            # If there are errors, render the form with the error messages
            context = {
                'user_form': user_form,
                'company_form': company_form,
                'user_info_form': user_info_form
            }
            return render(request, "users/new-applicant.html", context)
    else:
        user_form = ApplicantForm()
        user_info_form = UserInfoForm()
        company_form = CompanyForm()

    context = {
        'user_form': user_form,
        'user_info_form': user_info_form,
        'company_form': company_form
    }
    return render(request, "users/new-recruiter.html", context)


# Login User
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_state = get_object_or_404(User, username=email)

        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user_state)
            user_info = get_object_or_404(UserInfo, user=user)
            if user_info.is_applicant:
                return redirect('applicant-dash')
            elif user_info.is_recruiter:
                return redirect('recruiter-dash')
        else:
            messages.warning(request, "Invalid email or password.")

        return redirect("login")
    else:
        return render(request, "users/login.html")


# Logout User
def logout_user(request):
    logout(request)
    messages.info(request, "Your session has ended.")
    return redirect("index")
