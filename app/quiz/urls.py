from django.urls import path

from .views import quiz_questions, quiz_results


urlpatterns = [
    path("<str:persona>/", quiz_results, name="quiz-results"),
    path("question/<int:ref>/", quiz_questions, name="questions")
]
