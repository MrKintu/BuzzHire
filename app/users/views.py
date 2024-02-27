from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from company.models import Company, Company_Industry
from resume.models import Resume, Applicant_Industry
from users.models import UserInfo


# Register Applicant
def new_applicant(request):
    if request.method == "POST":
        data = request.POST
        if data["password1"] == data["password2"]:
            user = User.objects.create_user(
                username=data["email"],
                password=data["password1"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            user.save()
            user_state = User.objects.get(username=data["email"])

            new_file = request.FILES["resume"]
            ext1 = new_file.name.split('.')[-1]
            if ext1 != "pdf":
                messages.warning(request, "Upload failed. Please upload in pdf format.")
            resume_model = Resume()
            resume_model.user = user_state
            industry = Applicant_Industry.objects.get(name=data["industry"])
            resume_model.industry = industry
            resume_model.profession = data["profession"]
            resume_model.years = data["years"]
            resume_model.resume = new_file
            resume_model.street = data["street"]
            resume_model.city = data["city"]
            resume_model.zipcode = data["zipcode"]
            resume_model.state = data["state"]
            resume_model.country = data["country"]
            resume_model.phone = f'{data["code"]}-{data["phone"]}'
            resume_model.save()

            user_model = UserInfo()
            user_model.user = user_state
            if data["title"] == "1":
                user_model.title = "Mr"
            elif data["title"] == "2":
                user_model.title = "Mrs"
            else:
                user_model.title = "Ms"
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
            messages.warning(request, "Account creation failed! Passwords must match.")
            return redirect("new-applicant")
    else:
        return render(request, "users/new-applicant.html")


# Register Recruiter
def new_recruiter(request):
    if request.method == "POST":
        data = request.POST
        if data["password1"] == data["password2"]:
            user = User.objects.create_user(
                username=data["email"],
                password=data["password1"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            user.save()
            user_state = User.objects.get(username=data["email"])

            company_model = Company()
            company_model.user = user_state
            role = data["type"]
            if role == "1":
                company_model.type = "Staff"
            else:
                company_model.type = "Recruiter"
            company_model.company = data["company"]
            industry = Company_Industry.objects.get(name=data["industry"])
            company_model.industry = industry
            company_model.role = data["role"]
            company_model.website = data["website"]
            company_model.street = data["street"]
            company_model.city = data["city"]
            company_model.zipcode = data["zipcode"]
            company_model.state = data["state"]
            company_model.country = data["country"]
            company_model.phone = f'{data["code"]}-{data["phone"]}'
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
                return redirect("new-recruiter")
        else:
            messages.warning(request, "Account creation failed! Passwords must match.")
            return redirect("new-recruiter")
    else:
        return render(request, "users/new-recruiter.html")


# Login User
def login_user(request):
    if request.method == "POST":
        data = request.POST
        email = data["email"]
        password = data["password"]

        new_user = authenticate(request, username=email, password=password)
        if new_user is not None:
            login(request, new_user)
            user_state = User.objects.get(username=email)
            user_info = UserInfo.objects.get(user=user_state)
            if user_info.is_applicant:
                return redirect('applicant-dash')
            elif user_info.is_recruiter:
                return redirect('recruiter-dash')
            else:
                messages.warning(request, "Something went wrong...")
                return redirect("login")
        else:
            messages.warning(request, "Something went wrong...")
            return redirect("login")
    else:
        return render(request, "users/login.html")


# Logout User
def logout_user(request):
    logout(request)
    messages.info(request, "Your session has ended.")
    return redirect("index")
