from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from quiz.models import UserPersonality
from .models import MentorProfile

def find_mentors_for(user, top_n=3):
    """
    Finds the top N most compatible mentors for a given user based on personality traits.
    """
    try:
        mentee_personality = UserPersonality.objects.get(user=user)
        mentee_vector = np.array(mentee_personality.get_trait_vector()).reshape(1, -1)
    except UserPersonality.DoesNotExist:
        # If the user hasn't taken the quiz, we can't find matches.
        return []

    # Find all active mentors who have also completed the personality quiz.
    mentor_profiles = MentorProfile.objects.filter(
        user__userinfo__is_mentor=True,
        user__userpersonality__isnull=False
    ).select_related('user', 'user__userpersonality')

    mentor_scores = []
    for mentor_profile in mentor_profiles:
        mentor_personality = mentor_profile.user.userpersonality
        mentor_vector = np.array(mentor_personality.get_trait_vector()).reshape(1, -1)
        
        # Calculate cosine similarity
        sim_score = cosine_similarity(mentee_vector, mentor_vector)[0][0]
        mentor_scores.append((mentor_profile, sim_score))

    # Sort mentors by similarity score in descending order
    mentor_scores.sort(key=lambda x: x[1], reverse=True)

    # Return the top N mentor profiles
    return [profile for profile, score in mentor_scores[:top_n]]
