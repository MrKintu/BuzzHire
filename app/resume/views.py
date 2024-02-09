from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Resume


# @login_required
def edit_resume(request):
    if request.method == "POST":
        data = request.POST
        user = request.user
        # if user.is_authenticated:
        #     pass
        # else:
        #     pass
        user_state = User.objects.get(username=user.username)
        resume = Resume.objects.get(user=user_state)

        new_file = request.FILES["resume"]
        ext1 = new_file.name.split('.')[-1]
        if ext1 != "pdf":
            messages.warning(request, "Upload failed. Please upload in pdf format.")
        resume.industry = data["industry"]
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
        # if user.is_authenticated:
        #     pass
        # else:
        #     pass
        user_state = User.objects.get(username=user.username)
        resume = Resume.objects.get(user=user_state)

        send = {
            "first_name": user_state.first_name,
            "last_name": user_state.last_name,
            "email": user_state.email,
            "industry": resume.industry,
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
