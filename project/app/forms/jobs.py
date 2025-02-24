from django import forms
from .models import JobApplication

class ApplicationForm(forms.ModelForm):
    """
    Form for submitting a job application.
    """
    class Meta:
        model = JobApplication
        fields = ["name", "email", "resume", "cover_letter"]

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    resume = forms.FileField(required=False)
    cover_letter = forms.CharField(widget=forms.Textarea, required=True)