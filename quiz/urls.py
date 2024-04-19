from django.urls import path

from .views import quiz_questions, quiz_results, persona_chart


urlpatterns = [
    path("<str:persona>/", quiz_results, name="quiz-results"),
    path("question/<int:ref>/", quiz_questions, name="questions"),
    path("persona-chart/<int:ref>/", persona_chart, name="persona-chart")
]
