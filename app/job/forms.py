from django import forms
from .models import JobPost


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ['company', 'available']

    def clean_download(self):
        download = self.cleaned_data.get('download')
        if download:
            if not download.name.endswith('.pdf'):
                raise forms.ValidationError("Please upload a PDF file.")
        return download


class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ['company']

    def clean_download(self):
        download = self.cleaned_data.get('download')
        if download:
            if not download.name.endswith('.pdf'):
                raise forms.ValidationError("Please upload a PDF file.")
        return download
