from django import forms
from .models import MentorProfile

class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us a bit about your experience and what you can help with...'}),
        }
