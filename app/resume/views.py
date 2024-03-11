import secrets
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from job.models import JobPost, ApplyJob
from users.forms import ResumeForm, UserForm, UserInfoForm
from users.models import UserInfo
from .emailHandler import ApplicantEmail, RecruiterEmail
from .models import Resume


# Edit User Resume
@login_required
def edit_resume(request):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    resume = get_object_or_404(Resume, user=user)
    user_form = UserForm(instance=user)
    resume_form = ResumeForm(instance=resume)
    user_info_form = UserInfoForm(instance=user_info)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        resume_form = ResumeForm(request.POST, request.FILES, instance=resume)
        user_info_form = UserInfoForm(request.POST, instance=user_info)
        print(user_form.errors)
        if user_form.is_valid() and resume_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()

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

    # If it's a GET request or the form submission failed, render the form
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
        if ApplyJob.objects.filter(resume__user=user, job=job_post).exists():
            applied = True
            messages.info(request, "You have already applied for this job.")

        send = {
            "pk": pk,
            "company": job_post.company.company,
            "title": job_post.job_title,
            "industry": job_post.industry,
            "city": job_post.city,
            "state": job_post.state,
            "country": job_post.country,
            "pay": job_post.pay,
            "describe": job_post.describe,
            "tasks": job_post.tasks,
            "ideal": job_post.ideal_candidate,
            "download": job_post.download,
            "timestamp": job_post.timestamp,
            "applied": applied
        }

        return render(request, "resume/view-job.html", send)


def new_reference():
    alphabet = string.ascii_letters + string.digits
    secure_string = ''.join(secrets.choice(alphabet) for _ in range(16))
    reference = f"REF-{secure_string}"

    return reference


# Apply to job posting
@login_required
def apply_to_job(request, pk):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    job_post = get_object_or_404(JobPost, pk=pk)
    if ApplyJob.objects.filter(resume__user=user, job=job_post).exists():
        messages.warning(request, "Permission Denied.")
        return redirect("applicant-dash")
    resume = get_object_or_404(Resume, user=user)

    application = ApplyJob()
    application.job = job_post
    application.resume = resume
    application.status = "Pending"
    application.reference = new_reference()
    application.save()

    applicant_data = {
        "first_name": resume.user.first_name,
        "last_name": resume.user.last_name,
        "email": resume.user.email,
        "job_title": job_post.job_title,
        "company": job_post.company.company,
        "reference": application.reference
    }
    recruiter_data = {
        "email": job_post.company.user.email,
        "job_title": job_post.job_title,
        "company": job_post.company.company,
        "reference": application.reference
    }
    applicant_email = ApplicantEmail(applicant_data)
    recruiter_email = RecruiterEmail(recruiter_data)

    if applicant_email and recruiter_email:
        messages.success(request, "You have successfully applied for this role!")
        return redirect("applicant-dash")
    else:
        messages.warning(request, "Something went wrong, please try again.")
        return redirect("answers", pk=pk)


# View roles applied to.
@login_required
def jobs_applied(request):
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
        applied = ApplyJob.objects.filter(resume__user=user)

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
