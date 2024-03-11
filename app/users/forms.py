from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from company.models import Company
from resume.models import Resume
from .models import UserInfo


class ApplicantForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()  # Ensure email is lowercase

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username as email
        user.password = make_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ['user']

    def clean_download(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Please upload a PDF file.")
        return resume


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['title']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['user']
