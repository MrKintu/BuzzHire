from django.urls import path
from .views import find_mentor_view, become_mentor_view, mentor_profile_view, connect_with_mentor

urlpatterns = [
    path('find/', find_mentor_view, name='find-mentor'),
    path('become/', become_mentor_view, name='become-mentor'),
    path('profile/<int:user_id>/', mentor_profile_view, name='mentor-profile'),
    path('connect/<int:mentor_id>/', connect_with_mentor, name='connect-with-mentor'),
]
