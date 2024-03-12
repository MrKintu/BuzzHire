from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from users.models import UserInfo
from .forms import ResponseForm
from .models import Question, PersonalityType, Personality


@login_required
def quiz_questions(request, pk):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    if request.method == "POST":
        question = get_object_or_404(Question, pk=pk)
        count = pk

        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.user = user
            response.question = question
            response.dichotomy = question.dichotomy
            response.save()

            count += 1
            if count <= 100:
                return redirect("questions", pk=count)
            else:
                messages.success(request, "You have successfully completed the quiz!")
                return redirect("applicant-dash")
        else:
            messages.warning(request, "Something went wrong, please try again.")
            # If there are errors, render the form with the error messages
            context = {
                "question": question.text,
                "form": response_form
            }
            return render(request, "quiz/questions.html", context)
    else:
        question = get_object_or_404(Question, pk=pk)
        response_form = ResponseForm()

        context = {
            "question": question.text,
            "form": response_form
        }
        return render(request, "quiz/questions.html", context)


@login_required
def quiz_results(request, persona):
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
        person_type = get_object_or_404(PersonalityType, combo=persona)

        images = [
            "ENFJ_the_protagonist.jpg", "ENFP_the_campaigner.png", "ENTJ_the_commander.png", "ENTP_the_debater.jpg",
            "ESFJ_the_consul.png", "ESFP_the_entertainer.png", "ESTJ_the_executive.png", "ESTP_the_entrepreneur.png",
            "INFJ_the_advocate.png", "INFP_the_mediator.png", "INTJ_the_architect.jpg", "INTP_the_logician.jpg",
            "ISFJ_the_defender.png", "ISFP_the_adventurer.png", "ISTJ_the_logistician.png", "ISTP_the_virtuoso.png"
        ]
        image = next((img for img in images if img.startswith(persona)), None)

        personalities = []
        combo = list(persona)
        personality = Personality.objects.all()
        for x in range(len(personality)):
            single = personality[x]
            for y in range(len(combo)):
                letter = combo[y]
                if single.abbrv == letter:
                    data = {
                        "name": single.name,
                        "describe": single.describe
                    }
                    personalities.append(data)

        context = {
            "persona": persona,
            "image": image,
            "persona_type": person_type.name,
            "persona_describe": person_type.describe,
            "personalities": personalities
        }
        return render(request, "quiz/answer.html", context)
