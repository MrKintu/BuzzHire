from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from company.models import Company
from .models import JobPost


# Create a new job posting
def create_job(request):
    if request.method == "POST":
        data = request.POST
        user = request.user

        user_state = User.objects.get(username=user.username)
        company = Company.objects.get(user=user_state)
        new_file = request.FILES["download"]
        ext1 = new_file.name.split('.')[-1]
        if ext1 != "pdf":
            messages.warning(request, "Upload failed. Please upload in pdf format.")
            return redirect("new-job")

        new_job = JobPost()
        new_job.company = company
        new_job.created_by = user_state
        new_job.title = data["title"]
        new_job.industry = data["industry"]
        new_job.location = data["location"]
        new_job.pay = data["pay"]
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
        return render(request, "company/new-job.html")


# View Job Postings
def view_jobs(request):
    user = request.user
    user_state = User.objects.get(username=user.username)
    company = Company.objects.get(user=user_state)
    job_list = JobPost.objects.filter(company=company)

    send = []
    for x in range(len(job_list)):
        row = job_list[x]

        available = ""
        if row.available:
            available = "Yes"
        else:
            available = "No"

        single = {
            "pk": row.pk,
            "number": "100",
            "title": row.title,
            "location": row.location,
            "pay": str(row.pay),
            "available": available
        }
        send.append(single)

    data = {"data": send}
    return render(request, "company/view-jobs.html", data)


# Update Job Posting
def update_job(request, pk):
    if request.method == "POST":
        data = request.POST
        job_state = JobPost.objects.get(pk=pk)
        new_file = request.FILES["download"]
        ext1 = new_file.name.split('.')[-1]
        if ext1 != "pdf":
            messages.warning(request, "Upload failed. Please upload in pdf format.")
            return redirect('edit-job', pk)

        job_state.title = data["title"]
        job_state.industry = data["industry"]
        job_state.location = data["location"]
        job_state.pay = data["pay"]
        job_state.describe = data["describe"]
        job_state.tasks = data["tasks"]
        job_state.ideal = data["ideal"]
        job_state.download = new_file
        job_state.save()

        return redirect("recruiter-dash")
    else:
        job_state = JobPost.objects.get(pk=pk)
        data = {
            "pk": int(job_state.id),
            "available": job_state.available,
            "title": job_state.title,
            "industry": job_state.industry,
            "location": job_state.location,
            "pay": job_state.pay,
            "describe": job_state.describe,
            "tasks": job_state.tasks,
            "ideal": job_state.ideal
        }

        send = {"data": data}
        return render(request, "company/edit-job.html", send)


# Close Job Posting
def close_job(request, pk):
    job_state = JobPost.objects.get(pk=pk)
    job_state.available = False
    job_state.save()

    return redirect("view-jobs")


def open_job(request, pk):
    job_state = JobPost.objects.get(pk=pk)
    job_state.available = True
    job_state.save()

    return redirect("view-jobs")
