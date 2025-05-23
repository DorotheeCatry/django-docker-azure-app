from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.utils.html import format_html
from app.models import UserProfile

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            "name": "username",
            "placeholder": "Email Address",
            "required": True,
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
        }),
    )
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "name": "password",
            "placeholder": "Password",
            "required": True,
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
        }),
    )
    
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
    

class ChangePasswordForm(PasswordChangeForm):
    """
    Form for changing the user's password.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the ChangePasswordForm with custom labels, help text, and styles.
        """
        super().__init__(*args, **kwargs)

        self.fields["old_password"].label = "Current Password"
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password2"].label = "Confirm New Password"

        self.fields["new_password1"].help_text = format_html(
            '<ul classtext-sm text-gray-600 mt-2">'
            "<li>Your must be at least 8 characters long.</li>"
            "<li>Your cannot be entirely numeric.</li>"
            "<li>Your cannot be too similar to your other personal information.</li>"
            "</ul>")

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400",
                })