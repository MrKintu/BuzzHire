from django import forms
from .models import UserResponse


class ResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['response']
