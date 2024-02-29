from django import forms
from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ['created_by', 'company']

    def clean_download(self):
        download = self.cleaned_data.get('download')
        if download:
            if not download.name.endswith('.pdf'):
                raise forms.ValidationError("Please upload a PDF file.")
        return download
