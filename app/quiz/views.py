from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from resume.models import Resume
from users.models import UserInfo
from .fuzzyANN.plotGraph import GenerateChart
from .fuzzyANN.predictModel import PredictPersona
from .forms import ResponseForm
from .models import Question, PersonalityType, Personality, UserResponse, UserPersonality


@login_required
def quiz_questions(request, ref):
    user = request.user
    user_info = get_object_or_404(UserInfo, user=user)
    if not user_info.is_applicant:
        messages.warning(request, "You're not authorized to view that page!")
        return redirect("recruiter-dash")

    if request.method == "POST":
        question = get_object_or_404(Question, count=ref)
        count = ref

        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.user_info = user_info
            response.question = question
            response.dichotomy = question.dichotomy
            response.save()

            count += 1
            if count <= 100:
                return redirect("questions", ref=count)
            else:
                answers = UserResponse.objects.filter(user_info=user_info)
                personality = PredictPersona(answers)
                personality_type = get_object_or_404(PersonalityType, combo=personality["persona"])
                user_personality = UserPersonality()
                user_personality.user = user
                user_personality.persona = personality_type
                user_personality.introversion = personality["introversion"]
                user_personality.extroversion = personality["extroversion"]
                user_personality.sensing = personality["sensing"]
                user_personality.intuition = personality["intuition"]
                user_personality.thinking = personality["thinking"]
                user_personality.feeling = personality["feeling"]
                user_personality.judging = personality["judging"]
                user_personality.perceiving = personality["perceiving"]
                user_personality.save()

                resume = get_object_or_404(Resume, user=user)
                applicant_persona = get_object_or_404(PersonalityType, combo=personality["persona"])
                resume.personality = applicant_persona
                resume.save()

                messages.success(request, "You have successfully completed the quiz!")
                return redirect("quiz-results", persona=personality["persona"])
        else:
            messages.warning(request, "Something went wrong, please try again.")
            # If there are errors, render the form with the error messages
            context = {
                "question": question.text,
                "form": response_form
            }
            return render(request, "quiz/questions.html", context)
    else:
        question = get_object_or_404(Question, count=ref)
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


@login_required
def persona_chart(request, ref):
    if request.method == "POST":
        data = request.POST
        user_query = data["search"]
        return redirect("search", query=user_query)
    else:
        persona = get_object_or_404(UserPersonality, pk=ref)
        personality_percentages = [persona.introversion, persona.extroversion, persona.sensing, persona.intuition,
                                   persona.thinking, persona.feeling, persona.judging, persona.perceiving]
        personality_chart = GenerateChart(personality_percentages)

        user = request.user
        user_info = get_object_or_404(UserInfo, user=user)
        switch = False
        if user_info.is_applicant:
            switch = True

        send = {
            "switch": switch,
            "first_name": persona.user.first_name,
            "last_name": persona.user.last_name,
            'chart_data': personality_chart
        }
        return render(request, 'quiz/radar-chart.html', send)
