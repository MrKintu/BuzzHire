from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Resume, Applicant_Industry
from job.models import JobPost, ApplyJob
from company.models import Company
from users.models import UserInfo


# Edit User Resume
@login_required
def edit_resume(request):
    if request.method == "POST":
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_applicant:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("recruiter-dash")

        data = request.POST
        resume = Resume.objects.get(user=user_state)
        new_file = request.FILES["resume"]
        ext1 = new_file.name.split('.')[-1]
        if ext1 != "pdf":
            messages.warning(request, "Upload failed. Please upload in pdf format.")
            return redirect("edit-resume")

        industry = Applicant_Industry.objects.get(name=data["industry"])
        resume.industry = industry
        resume.profession = data["profession"]
        resume.years = data["years"]
        resume.resume = new_file
        resume.phone = data["phone"]
        resume.street = data["street"]
        resume.city = data["city"]
        resume.country = data["country"]
        resume.state = data["state"]
        resume.zipcode = data["zipcode"]
        resume.save()

        messages.success(request, "Account has been successfully updated!")
        return redirect("applicant-dash")
    else:
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_applicant:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("recruiter-dash")

        resume = Resume.objects.get(user=user_state)

        send = {
            "first_name": user_state.first_name,
            "last_name": user_state.last_name,
            "email": user_state.email,
            "industry": resume.industry.name,
            "profession": resume.profession,
            "years": resume.years,
            "resume": resume.resume,
            "phone": resume.phone,
            "street": resume.street,
            "city": resume.city,
            "country": resume.country,
            "state": resume.state,
            "zipcode": resume.zipcode
        }
        return render(request, "resume/edit-resume.html", send)


# View Job Posting
@login_required
def job_details(request, pk):
    if request.method == "POST":
        data = request.POST
        user_query = data["search"]

        return redirect("search", query=user_query)
    else:
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_applicant:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("recruiter-dash")

        job_post = JobPost.objects.get(pk=pk)
        applied = False
        if ApplyJob.objects.filter(user=user_state, job=job_post).exists():
            applied = True
            messages.info(request, "You have already applied for this job.")

        send = {
            "pk": pk,
            "company": job_post.company.company,
            "title": job_post.title,
            "industry": job_post.industry.name,
            "city": job_post.city,
            "state": job_post.state,
            "country": job_post.country,
            "pay": job_post.pay,
            "describe": job_post.describe,
            "tasks": job_post.tasks,
            "ideal": job_post.ideal,
            "download": job_post.download,
            "timestamp": job_post.timestamp,
            "applied": applied
        }

        return render(request, "resume/view-job.html", send)


# Apply to job posting
@login_required
def apply_to_job(request, pk):
    user = request.user
    user_state = User.objects.get(username=user.username)
    user_info = UserInfo.objects.get(user=user_state)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("recruiter-dash")

    job_post = JobPost.objects.get(pk=pk)
    if ApplyJob.objects.filter(user=user_state, job=job_post).exists():
        messages.warning(request, "Permission Denied.")
        return redirect("applicant-dash")

    application = ApplyJob()
    application.user = user_state
    application.job = job_post
    application.status = "Pending"
    application.save()

    messages.success(request, "You have successfully applied for this role!")
    return redirect("applicant-dash")


@login_required
def jobs_applied(request):
    user = request.user
    user_state = User.objects.get(username=user.username)
    user_info = UserInfo.objects.get(user=user_state)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("recruiter-dash")

    applied = ApplyJob.objects.filter(user=user_state)
    job_list = []
    for x in range(len(applied)):
        single = applied[x]
        details = {
            "pk": single.job.pk,
            "title": single.job.title,
            "company": single.job.company.company,
            "industry": single.job.industry.name,
            "timestamp": single.timestamp,
            "city": single.job.city,
            "state": single.job.state,
            "country": single.job.country,
            "available": single.job.available,
            "status": single.status
        }
        job_list.append(details)

    send = {"data": job_list}
    return render(request, "resume/jobs-applied.html", send)
