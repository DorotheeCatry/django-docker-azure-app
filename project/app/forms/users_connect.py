from django import forms
from django.contrib.auth.hashers import make_password
from app.models import UserProfile

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ["username", "email", "first_name", "last_name", "role"]


class UserSignupForm(forms.ModelForm):
    """
    Form for user signup.
    """
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )

    class Meta:
        model = UserProfile
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")