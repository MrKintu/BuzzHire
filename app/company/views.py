from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from job.models import JobPost, ApplyJob
from resume.models import Resume
from users.forms import ApplicantForm, UserInfoForm, CompanyForm
from users.models import UserInfo
from .models import Company


# Edit Company Details
@login_required
def edit_company(request):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    if request.method == "POST":
        user_form = ApplicantForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        company_form = CompanyForm(request.POST)

        if user_form.is_valid() and user_info_form.is_valid() and company_form.is_valid():
            user = user_form.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.is_recruiter = True
            user_info.has_company = True
            user_info.save()

            company = company_form.save(commit=False)
            company.user = user
            company.save()

            messages.success(request, "Your account has successfully been updated.")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong, please try again.")
            # If there are errors, render the form with the error messages
            context = {
                'user_form': user_form,
                'company_form': company_form,
                'user_info_form': user_info_form
            }
            return render(request, "company/edit-company.html", context)
    else:
        company = get_object_or_404(Company, user=user)
        user_form = ApplicantForm(instance=user)
        company_form = CompanyForm(instance=company)
        user_info_form = UserInfoForm(instance=user_info)
        context = {
            'user_form': user_form,
            'company_form': company_form,
            'user_info_form': user_info_form
        }
        return render(request, "company/edit-company.html", context)


# View All applicants for a role
@login_required
def all_applicants(request, pk):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    job_post = get_object_or_404(JobPost, pk=pk)
    applicants = ApplyJob.objects.filter(job=job_post).order_by("-timestamp")

    paginator = Paginator(applicants, 10)  # Show 10 applicants per page
    page = request.GET.get('page')
    try:
        applicants = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        applicants = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        applicants = paginator.page(paginator.num_pages)

    context = {
        "data": applicants,
        "pk": pk,
    }

    return render(request, "company/results.html", context)


# View Single Application
@login_required
def single_applicant(request, pk):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_recruiter:
        messages.warning(request, "You're not authorised to view that page!")
        return redirect("applicant-dash")

    if request.method == "POST":
        data = request.POST
        apply_job = get_object_or_404(ApplyJob, pk=pk)

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
        apply_job = get_object_or_404(ApplyJob, pk=pk)
        app_user = get_object_or_404(User, pk=apply_job.user.pk)
        resume = get_object_or_404(Resume, user=app_user)
        user_info = get_object_or_404(UserInfo, user=app_user)

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
