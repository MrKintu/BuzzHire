from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from company.models import Company
from job.models import JobPost, ApplyJob
from quiz.models import UserPersonality
from resume.models import Resume
from users.models import UserInfo


# Index Page
def index(request):
    if request.method == "POST":
        data = request.POST
        user_query = data["search"]
        return redirect("search", query=user_query)
    else:
        user = request.user
        switch = False
        if user.is_authenticated:
            user_info = get_object_or_404(UserInfo, user=user)
            if user_info.is_applicant:
                switch = True

        jobs = JobPost.objects.all().order_by("-timestamp")
        paginator = Paginator(jobs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        send = {
            "switch": switch,
            "page_obj": page_obj
        }
        return render(request, "dashboard/index.html", send)


# Applicant Dashboard
@login_required
def applicant_dash(request):
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
        resume = get_object_or_404(Resume, user=user)
        applications = ApplyJob.objects.filter(resume=resume)
        app_count = applications.count()
        approved = applications.filter(status="Approved").count()
        declined = applications.filter(status="Declined").count()
        pending = applications.exclude(status__in=["Approved", "Declined"]).count()
        images = [
            "ENFJ_the_protagonist.jpg", "ENFP_the_campaigner.png", "ENTJ_the_commander.png", "ENTP_the_debater.jpg",
            "ESFJ_the_consul.png", "ESFP_the_entertainer.png", "ESTJ_the_executive.png", "ESTP_the_entrepreneur.png",
            "INFJ_the_advocate.png", "INFP_the_mediator.png", "INTJ_the_architect.jpg", "INTP_the_logician.jpg",
            "ISFJ_the_defender.png", "ISFP_the_adventurer.png", "ISTJ_the_logistician.png", "ISTP_the_virtuoso.png"
        ]
        test, persona, image = False, "", ""
        if resume.personality:
            test = True
            persona = resume.personality.combo
            image = next((img for img in images if img.startswith(persona)), None)

        ref = ""
        if UserPersonality.objects.filter(user=user).exists():
            user_personality = get_object_or_404(UserPersonality, user=user)
            ref = user_personality.pk

        send = {
            "title": user_info.title,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": resume.user.email,
            "phone": resume.phone,
            "profession": resume.profession,
            "industry": resume.industry,
            "years": resume.years,
            "street": resume.street,
            "city": resume.city,
            "state": resume.state,
            "country": resume.country,
            "zipcode": resume.zipcode,
            "resume": resume.resume,
            "applications": app_count,
            "approved": approved,
            "declined": declined,
            "pending": pending,
            "test": test,
            "image": image,
            "persona": persona,
            "ref": ref
        }

        return render(request, "dashboard/applicant-dash.html", send)


# Recruiter Dashboard
@login_required
def recruiter_dash(request):
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
        job_list = JobPost.objects.filter(company=company)
        job_count = job_list.filter(available=True).count()
        disabled = job_list.filter(available=False).count()
        applications = ApplyJob.objects.filter(job__in=job_list)
        app_count = applications.count()
        approved = applications.filter(status="Approved").count()
        declined = applications.filter(status="Declined").count()
        pending = applications.exclude(status__in=["Approved", "Declined"]).count()

        send = {
            "title": user_info.title,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": company.phone,
            "type": company.recruiter_type,
            "company": company.company,
            "industry": company.industry,
            "role": company.role,
            "website": company.website,
            "street": company.street,
            "city": company.city,
            "state": company.state,
            "country": company.country,
            "zipcode": company.zipcode,
            "posts": job_list.count(),
            "available": job_count,
            "disabled": disabled,
            "applications": app_count,
            "approved": approved,
            "declined": declined,
            "pending": pending
        }

        return render(request, "dashboard/recruiter-dash.html", send)


# Search for Job Posting
def search(request, query):
    if request.method == "POST":
        data = request.POST
        user_query = data["search"]
        return redirect("search", query=user_query)
    else:
        user = request.user
        switch = False
        if user.is_authenticated:
            user_info = get_object_or_404(UserInfo, user=user)
            if user_info.is_applicant:
                switch = True

        titles = JobPost.objects.filter(job_title__icontains=query)
        cities = JobPost.objects.filter(city__icontains=query)
        states = JobPost.objects.filter(state__icontains=query)
        countries = JobPost.objects.filter(country__icontains=query)
        industries = JobPost.objects.filter(industry__icontains=query)

        job_posts = titles | cities | states | countries | industries
        job_posts = job_posts.order_by("-timestamp")

        paginator = Paginator(job_posts, 5)  # 5 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        send = {
            "query": query,
            "switch": switch,
            "page_obj": page_obj
        }
        return render(request, "dashboard/search.html", send)

