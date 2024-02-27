from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from company.models import Company
from users.models import UserInfo
from .models import JobPost, ApplyJob, Job_Industry


# Create a new job posting
@login_required
def create_job(request):
    if request.method == "POST":
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        data = request.POST
        company = Company.objects.get(user=user_state)
        new_file = request.FILES["download"]
        ext1 = new_file.name.split('.')[-1]
        if ext1 != "pdf":
            messages.warning(request, "Upload failed. Please upload in pdf format.")
            return redirect("new-job")
        industry = Job_Industry.objects.get(name=data["industry"])

        new_job = JobPost()
        new_job.company = company
        new_job.created_by = user_state
        new_job.title = data["title"]
        new_job.industry = industry
        new_job.city = data["city"]
        new_job.state = data["state"]
        new_job.country = data["country"]
        new_job.pay = data["pay"]
        new_job.job_type = data["type"]
        new_job.describe = data["describe"]
        new_job.tasks = data["tasks"]
        new_job.ideal = data["ideal"]
        new_job.available = True
        new_job.download = new_file
        new_job.save()

        if JobPost.objects.filter(company=company).exists() and JobPost.objects.filter(created_by=user_state).exists():
            messages.success(request, "Your new job posting has successfully been created.")
            return redirect("recruiter-dash")
        else:
            messages.warning(request, "Something went wrong, please try again.")
            return redirect("new-job")
    else:
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        return render(request, "company/new-job.html")


# View Job Postings
@login_required
def list_jobs(request):
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

        company = Company.objects.get(user=user_state)
        job_list = JobPost.objects.filter(company=company).order_by("-timestamp")

        send = []
        for x in range(len(job_list)):
            single = job_list[x]
            applicants = ApplyJob.objects.filter(job=single).count()
            if single.available:
                available = "Yes"
            else:
                available = "No"

            single = {
                "pk": single.pk,
                "number": applicants,
                "title": single.title,
                "city": single.city,
                "state": single.state,
                "country": single.country,
                "industry": single.industry.name,
                "pay": single.pay,
                "available": available,
                "timestamp": single.timestamp
            }
            send.append(single)

        data = {"data": send}
        return render(request, "company/list-jobs.html", data)


# Update Job Posting
@login_required
def update_job(request, pk):
    if request.method == "POST":
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

        data = request.POST
        job_state = JobPost.objects.get(pk=pk)
        industry = Job_Industry.objects.get(name=data["industry"])
        new_file = request.FILES["download"]
        ext1 = new_file.name.split('.')[-1]
        if ext1 != "pdf":
            messages.warning(request, "Upload failed. Please upload in pdf format.")
            return redirect('edit-job', pk)

        job_state.title = data["title"]
        job_state.industry = industry
        job_state.city = data["city"]
        job_state.state = data["state"]
        job_state.country = data["country"]
        job_state.pay = data["pay"]
        job_state.job_type = data["type"]
        job_state.describe = data["describe"]
        job_state.tasks = data["tasks"]
        job_state.ideal = data["ideal"]
        job_state.download = new_file
        job_state.save()

        return redirect("recruiter-dash")
    else:
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")
        job_state = JobPost.objects.get(pk=pk)

        send = {
            "pk": pk,
            "available": job_state.available,
            "title": job_state.title,
            "city": job_state.city,
            "state": job_state.state,
            "country": job_state.country,
            "pay": job_state.pay,
            "type": job_state.job_type,
            "describe": job_state.describe,
            "tasks": job_state.tasks,
            "ideal": job_state.ideal,
            "download": job_state.download,
            "filename": job_state.download.name[5:]
        }

        return render(request, "company/edit-job.html", send)


# Close Job Posting
def close_job(request, pk):
    job_state = JobPost.objects.get(pk=pk)
    job_state.available = False
    job_state.save()

    return redirect("list-jobs")


def open_job(request, pk):
    job_state = JobPost.objects.get(pk=pk)
    job_state.available = True
    job_state.save()

    return redirect("list-jobs")
