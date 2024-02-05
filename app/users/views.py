from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from company.models import Company
from resume.models import Resume
from users.models import UserInfo


# Register Applicant
def new_applicant(request):
    if request.method == "POST":
        data = request.POST
        user = User.objects.create_user(
            username=data["email"],
            password=data["password"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )
        user.save()
        user_state = User.objects.get(username=data["email"])

        newFile = request.FILES['resume']
        ext1 = newFile.name.split('.')[-1]
        if ext1 != "pdf":
            messages.warning(request, "Upload failed. Please upload in pdf format.")
        resume_model = Resume()
        resume_model.user = user_state
        resume_model.industry = data["industry"]
        resume_model.profession = data["profession"]
        resume_model.years = data["years"]
        resume_model.resume = newFile
        resume_model.street = data["street"]
        resume_model.zipcode = data["zipcode"]
        resume_model.state = data["state"]
        resume_model.country = data["country"]
        resume_model.phone = data["phone"]
        resume_model.save()

        user_model = UserInfo()
        user_model.user = user_state
        user_model.title = data["title"]
        user_model.is_applicant = True
        user_model.has_resume = True
        user_model.save()

        if (User.objects.filter(username=data["email"]).exists()
                and Resume.objects.filter(user=user_state).exists()
                and UserInfo.objects.filter(user=user_state).exists()):
            messages.success(request, "Your account has successfully been created.")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong, please try again.")
            return redirect("new-applicant")
    else:
        return render(request, "users/new-applicant.html")


# Register Recruiter
def new_recruiter(request):
    if request.method == "POST":
        data = request.POST
        user = User.objects.create_user(
            username=data["email"],
            password=data["password"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )
        user.save()
        user_state = User.objects.get(username=data["email"])

        company_model = Company()
        company_model.user = user_state
        company_model.type = data["type"]
        company_model.company = data["company"]
        company_model.industry = data["industry"]
        company_model.role = data["role"]
        company_model.website = data["website"]
        company_model.address = data["address"]
        company_model.city = data["city"]
        company_model.zipcode = data["zipcode"]
        company_model.state = data["state"]
        company_model.country = data["country"]
        company_model.phone = data["phone"]
        company_model.save()

        user_model = UserInfo()
        user_model.user = user_state
        user_model.title = data["title"]
        user_model.is_recruiter = True
        user_model.has_company = True
        user_model.save()

        if (User.objects.filter(username=data["email"]).exists()
                and Company.objects.filter(user=user_state).exists()
                and UserInfo.objects.filter(user=user_state).exists()):
            messages.success(request, "Your account has successfully been created.")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong, please try again.")
            return redirect("new-applicant")
    else:
        return render(request, "users/new-recruiter.html")


# Login User
def login_user(request):
    if request.method == "POST":
        data = request.POST
        email = data["email"]
        password = data["password"]

        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.warning(request, "Something went wrong...")
            return redirect("login")
    else:
        return render(request, "users/login.html")


# Logout User
def logout_user(request):
    logout(request)
    messages.info(request, "Your session has ended.")
    return redirect("login")
