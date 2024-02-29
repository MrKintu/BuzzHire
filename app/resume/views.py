from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from job.models import JobPost, ApplyJob
from users.forms import ResumeForm, ApplicantForm, UserInfoForm
from users.models import UserInfo
from .models import Resume


# Edit User Resume
@login_required
def edit_resume(request):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    if request.method == "POST":
        user_form = ApplicantForm(request.POST)
        resume_form = ResumeForm(request.POST, request.FILES)
        user_info_form = UserInfoForm(request.POST)

        if user_form.is_valid() and resume_form.is_valid() and user_info_form.is_valid():
            user = user_form.save(commit=False)
            user.save()

            resume = resume_form.save(commit=False)
            resume.user = user
            resume.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.is_applicant = True
            user_info.has_resume = True
            user_info.save()

            messages.success(request, "Your account has successfully been updated.")
            return redirect("applicant-dash")
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
        resume = get_object_or_404(Resume, user=user)
        user_form = ApplicantForm(instance=user)
        resume_form = ResumeForm(instance=resume)
        user_info_form = UserInfoForm(instance=user_info)
        context = {
            'user_form': user_form,
            'resume_form': resume_form,
            'user_info_form': user_info_form
        }

        return render(request, "resume/edit-resume.html", context)


# View Job Posting
@login_required
def job_details(request, pk):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    if request.method == "POST":
        data = request.POST
        user_query = data["search"]

        return redirect("search", query=user_query)
    else:
        job_post = get_object_or_404(JobPost, pk=pk)
        applied = False
        if ApplyJob.objects.filter(user=user, job=job_post).exists():
            applied = True
            messages.info(request, "You have already applied for this job.")

        send = {
            "pk": pk,
            "company": job_post.company.company,
            "title": job_post.job_title,
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
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    job_post = get_object_or_404(JobPost, pk=pk)
    if ApplyJob.objects.filter(user=user, job=job_post).exists():
        messages.warning(request, "Permission Denied.")
        return redirect("applicant-dash")
    resume = get_object_or_404(Resume, user=user)

    application = ApplyJob()
    application.job = job_post
    application.resume = resume
    application.status = "Pending"
    application.save()

    messages.success(request, "You have successfully applied for this role!")
    return redirect("applicant-dash")


# View roles applied to.
@login_required
def jobs_applied(request):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    applied = ApplyJob.objects.filter(user=user)

    # Paginate the queryset
    paginator = Paginator(applied, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    try:
        job_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        job_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        job_list = paginator.page(paginator.num_pages)

    send = {"data": job_list}
    return render(request, "resume/jobs-applied.html", send)
