from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MentorProfile, MentorshipConnection
from .forms import MentorProfileForm
from .matching import find_mentors_for
from users.models import UserInfo, User


@login_required
def find_mentor_view(request):
    """
    Finds and displays a list of recommended mentors for the logged-in user.
    """
    recommended_mentors = find_mentors_for(request.user)
    context = {
        'mentors': recommended_mentors,
    }
    return render(request, 'mentorship/find_mentor.html', context)


@login_required
def become_mentor_view(request):
    """
    Handles the process for a user to become a mentor.
    """
    user_info = get_object_or_404(UserInfo, user=request.user)
    if user_info.is_mentor:
        messages.info(request, "You are already a mentor.")
        return redirect('applicant-dash')

    if request.method == 'POST':
        form = MentorProfileForm(request.POST)
        if form.is_valid():
            # Mark the user as a mentor
            user_info.is_mentor = True
            user_info.save()

            # Create their mentor profile
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(request, "Congratulations! You are now a mentor.")
            return redirect('applicant-dash')
    else:
        form = MentorProfileForm()

    context = {'form': form}
    return render(request, 'mentorship/become_mentor.html', context)


@login_required
def mentor_profile_view(request, user_id):
    """
    Displays the public profile of a mentor.
    """
    mentor_profile = get_object_or_404(MentorProfile, user_id=user_id)
    is_connected = MentorshipConnection.objects.filter(
        mentor=mentor_profile.user,
        mentee=request.user
    ).exists()

    context = {
        'profile': mentor_profile,
        'is_connected': is_connected
    }
    return render(request, 'mentorship/mentor_profile.html', context)


@login_required
def connect_with_mentor(request, mentor_id):
    """
    Creates a connection between the logged-in user (mentee) and a mentor.
    """
    if request.method == 'POST':
        mentor_user = get_object_or_404(User, id=mentor_id)
        mentee_user = request.user

        if mentor_user == mentee_user:
            messages.error(request, "You cannot connect with yourself.")
            return redirect('mentor-profile', user_id=mentor_id)

        if MentorshipConnection.objects.filter(mentor=mentor_user, mentee=mentee_user).exists():
            messages.info(request, f"You are already connected with {mentor_user.username}.")
        else:
            MentorshipConnection.objects.create(mentor=mentor_user, mentee=mentee_user)
            messages.success(request, f"You have successfully connected with {mentor_user.username}!")
        
        return redirect('mentor-profile', user_id=mentor_id)
    else:
        return redirect('find-mentor')