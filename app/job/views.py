from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from company.models import Company
from users.models import UserInfo
from .forms import JobPostForm
from .models import JobPost, ApplyJob


# Create a new job posting
@login_required
def create_job(request):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    if request.method == "POST":
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            company = get_object_or_404(Company, user=user)
            new_job = form.save(commit=False)
            new_job.company = company
            new_job.created_by = user
            new_job.available = True
            new_job.save()
            messages.success(request, "Your new job posting has successfully been created.")
            return redirect("recruiter-dash")
        else:
            messages.warning(request, "Upload failed. Please upload in pdf format.")
            return redirect("new-job")
    else:
        form = JobPostForm()
        return render(request, "company/new-job.html", {"form": form})


# View Job Postings
@login_required
def list_jobs(request):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    if request.method == "POST":
        data = request.POST
        user_query = data["search"]
        return redirect("search", query=user_query)
    else:
        company = get_object_or_404(Company, user=user)
        job_list = JobPost.objects.filter(company=company).order_by("-timestamp")

        paginator = Paginator(job_list, 10)  # Number of items per page
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            jobs = paginator.page(paginator.num_pages)

        # Calculate applicants for each job in the paginated queryset
        for job in jobs:
            job.applicants = ApplyJob.objects.filter(job=job).count()

        send = {"data": jobs}  # Pass the paginated jobs to the template
        return render(request, "company/list-jobs.html", send)


# Update Job Posting
@login_required
def update_job(request, pk):
    user_info = get_object_or_404(UserInfo, user=request.user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    job_post = get_object_or_404(JobPost, pk=pk)
    form = JobPostForm(request.POST or None, request.FILES or None, instance=job_post)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Job post updated successfully!")
            return redirect("recruiter-dash")
        else:
            messages.error(request, "Failed to update job post. Please correct the errors.")

    context = {"form": form}
    return render(request, "company/edit-job.html", context)


# Close Job Posting
@login_required
def close_job(request, pk):
    user_info = get_object_or_404(UserInfo, user=request.user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    job_state = get_object_or_404(JobPost, pk=pk)
    job_state.available = False
    job_state.save()

    return redirect("list-jobs")


# Open Job Posting
@login_required
def open_job(request, pk):
    user_info = get_object_or_404(UserInfo, user=request.user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    job_state = get_object_or_404(JobPost, pk=pk)
    job_state.available = True
    job_state.save()

    return redirect("list-jobs")
