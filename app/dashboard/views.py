from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from company.models import Company
from job.models import JobPost, ApplyJob, Job_Industry
from resume.models import Resume
from users.models import UserInfo


def index(request):
    if request.method == "POST":
        data = request.POST
        user_query = data["search"]

        return redirect("search", query=user_query)
    else:
        user = request.user
        switch = bool
        if user.is_authenticated:
            jobs = JobPost.objects.all().order_by("-timestamp")
            user_state = User.objects.get(username=user.username)
            user_info = UserInfo.objects.get(user=user_state)
            if user_info.is_applicant:
                switch = True
            else:
                switch = False
        else:
            jobs = JobPost.objects.all().order_by("-timestamp")[:5]

        job_list = []
        for x in range(len(jobs)):
            job = jobs[x]

            data = {
                "title": job.title,
                "industry": job.industry.name,
                "company": job.company.company,
                "timestamp": job.timestamp,
                "city": job.city,
                "state": job.state,
                "country": job.country,
                "pay": job.pay,
                "website": job.company.website,
                "pk": job.pk
            }
            job_list.append(data)

        send = {
            "switch": switch,
            "data": job_list
        }
        return render(request, "dashboard/index.html", send)


@login_required
def applicant_dash(request):
    if request.method == "POST":
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_applicant:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("recruiter-dash")

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

        resume = Resume.objects.get(user=user_state)
        send = {
            "title": user_info.title,
            "first_name": user_state.first_name,
            "last_name": user_state.last_name,
            "email": user_state.email,
            "phone": resume.phone,
            "profession": resume.profession,
            "industry": resume.industry.name,
            "years": resume.years,
            "street": resume.street,
            "city": resume.city,
            "state": resume.state,
            "country": resume.country,
            "zipcode": resume.zipcode,
            "resume": resume.resume
        }

        return render(request, "dashboard/applicant-dash.html", send)


@login_required
def recruiter_dash(request):
    if request.method == "POST":
        user = request.user
        user_state = User.objects.get(username=user.username)
        user_info = UserInfo.objects.get(user=user_state)
        if not user_info.is_recruiter:
            messages.warning(request, "You're not authorised to view that page!")
            return redirect("applicant-dash")

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

        job_list = JobPost.objects.filter(company=company)
        job_count, app_count, disabled = 0, 0, 0
        approved, declined, pending = 0, 0, 0
        for x in range(len(job_list)):
            single = job_list[x]
            if single.available:
                job_count += 1
            else:
                disabled += 1

            applications = ApplyJob.objects.filter(job=single)
            if applications.exists():
                app_count = applications.count()
                for y in range(len(applications)):
                    app = applications[y]
                    if app.status == "Approved":
                        approved += 1
                    elif app.status == "Declined":
                        declined += 1
                    else:
                        pending += 1

        send = {
            "title": user_info.title,
            "first_name": user_state.first_name,
            "last_name": user_state.last_name,
            "email": user_state.email,
            "phone": company.phone,
            "type": company.type,
            "company": company.company,
            "industry": company.industry.name,
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


def search(request, query):
    if request.method == "POST":
        data = request.POST
        user_query = data["search"]

        return redirect("search", query=user_query)
    else:
        titles = JobPost.objects.filter(title__icontains=query)
        cities = JobPost.objects.filter(city__icontains=query)
        states = JobPost.objects.filter(state__icontains=query)
        countries = JobPost.objects.filter(country__icontains=query)
        industries = Job_Industry.objects.filter(name__icontains=query)
        if titles.exists() or cities.exists() or states.exists() or countries.exists() or industries.exists():
            job_posts = titles | cities | states | countries
            job_posts = job_posts.order_by("-timestamp")
            job_list = []

            for x in range(len(job_posts)):
                single = job_posts[x]
                data = {
                    "title": single.title,
                    "industry": single.industry.name,
                    "company": single.company.company,
                    "timestamp": single.timestamp,
                    "city": single.city,
                    "state": single.state,
                    "country": single.country,
                    "pay": single.pay,
                    "website": single.company.website,
                    "pk": single.pk,
                }
                job_list.append(data)

            for y in range(len(industries)):
                single = industries[y]
                jobs = JobPost.objects.filter(industry=single)
                for z in range(len(jobs)):
                    job = jobs[z]
                    data = {
                        "title": job.title,
                        "industry": job.industry.name,
                        "company": job.company.company,
                        "timestamp": job.timestamp,
                        "city": job.city,
                        "state": job.state,
                        "country": job.country,
                        "pay": job.pay,
                        "website": job.company.website,
                        "pk": job.pk,
                    }
                    job_list.append(data)

            send = {
                "query": query,
                "data": job_list
            }
            return render(request, "dashboard/search.html", send)
        else:
            messages.info(request, "We failed to match your query to a result.")
            return redirect("index")
