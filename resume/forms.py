from django import forms

from resume.models import Education, PastRoles


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['resume']


class RolesForm(forms.ModelForm):
    class Meta:
        model = PastRoles
        exclude = ['resume']
