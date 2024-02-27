from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from job.models import JobPost, ApplyJob
from resume.models import Resume
from users.models import UserInfo
from .models import Company, Company_Industry


# Edit Company Details
@login_required
def edit_company(request):
    if request.method == "POST":
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        data = request.POST
        company = Company.objects.get(user=user_state)
        industry = Company_Industry.objects.get(name=data["industry"])

        company.industry = industry
        company.phone = data["phone"]
        company.website = data["website"]
        company.street = data["street"]
        company.city = data["city"]
        company.country = data["country"]
        company.state = data["state"]
        company.zipcode = data["zipcode"]
        company.save()

        messages.success(request, "Account has been successfully updated!")
        return redirect("recruiter-dash")
    else:
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        company = Company.objects.get(user=user_state)

        send = {
            "first_name": user_state.first_name,
            "last_name": user_state.last_name,
            "email": user_state.email,
            "company": company.company,
            "role": company.role,
            "phone": company.phone,
            "website": company.website,
            "street": company.street,
            "city": company.city,
            "country": company.country,
            "state": company.state,
            "zipcode": company.zipcode
        }
        return render(request, "company/edit-company.html", send)


# View All applicants for a role
@login_required
def all_applicants(request, pk):
    if request.method == "POST":
        data = request.POST
        user_query = data["search"]

        return redirect("search", query=user_query)
    else:
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        job_post = JobPost.objects.get(pk=pk)
        applicants = ApplyJob.objects.filter(job=job_post).order_by("-timestamp")

        send = []
        for x in range(len(applicants)):
            single = applicants[x]
            app_user = User.objects.get(pk=single.user.pk)
            resume = Resume.objects.get(user=app_user)
            user_info = UserInfo.objects.get(user=app_user)

            details = {
                "pk": single.pk,
                "title": user_info.title,
                "first_name": app_user.first_name,
                "last_name": app_user.last_name,
                "profession": resume.profession,
                "industry": resume.industry.name,
                "email": app_user.email,
                "phone": resume.phone,
                "city": resume.city,
                "country": resume.country,
                "timestamp": single.timestamp,
                "status": single.status
            }
            send.append(details)

        data = {"data": send}
        return render(request, "company/results.html", data)


# View Single Application
def single_applicant(request, pk):
    if request.method == "POST":
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        data = request.POST
        apply_job = ApplyJob.objects.get(pk=pk)

        if data["decide"] == "1":
            apply_job.status = "Approved"
            apply_job.save()
            messages.success(request, "The applicant was successfully approved!")
        elif data["decide"] == "2":
            apply_job.status = "Declined"
            apply_job.save()
            messages.warning(request, "The applicant has been declined.")
        else:
            apply_job.status = "Pending"
            apply_job.save()
            messages.info(request, "The applicant shall remain pending.")

        return redirect("results", pk=pk)
    else:
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        apply_job = ApplyJob.objects.get(pk=pk)
        app_user = User.objects.get(pk=apply_job.user.pk)
        resume = Resume.objects.get(user=app_user)
        user_info = UserInfo.objects.get(user=app_user)

        details = {
            "pk": apply_job.job.pk,
            "title": user_info.title,
            "first_name": app_user.first_name,
            "last_name": app_user.last_name,
            "email": app_user.email,
            "phone": resume.phone,
            "profession": resume.profession,
            "industry": resume.industry.name,
            "years": resume.years,
            "street": resume.street,
            "city": resume.city,
            "zipcode": resume.zipcode,
            "state": resume.state,
            "country": resume.country,
            "resume": resume.resume,
            "timestamp": apply_job.timestamp
        }

        return render(request, "company/view-applicant.html", details)
