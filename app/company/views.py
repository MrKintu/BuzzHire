from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Company


# @login_required
def edit_company(request):
    if request.method == "POST":
        data = request.POST
        user = request.user
        # if user.is_authenticated:
        #     pass
        # else:
        #     pass
        user_state = User.objects.get(username=user.username)
        company = Company.objects.get(user=user_state)

        company.phone = data["phone"]
        company.website = data["website"]
        company.street = data["street"]
        company.city = data["city"]
        company.country = data["country"]
        company.state = data["state"]
        company.zipcode = data["zipcode"]
        company.save()

        messages.success(request, "Account has been successfully updated!")
        return redirect("recruiter-dash")
    else:
        user = request.user
        # if user.is_authenticated:
        #     pass
        # else:
        #     pass
        user_state = User.objects.get(username=user.username)
        company = Company.objects.get(user=user_state)

        send = {
            "first_name": user_state.first_name,
            "last_name": user_state.last_name,
            "email": user_state.email,
            "company": company.company,
            "role": company.role,
            "phone": company.phone,
            "website": company.website,
            "street": company.street,
            "city": company.city,
            "country": company.country,
            "state": company.state,
            "zipcode": company.zipcode
        }
        return render(request, "company/edit-company.html", send)
