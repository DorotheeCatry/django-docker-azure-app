from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.html import format_html

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
 "</ul>"
 )

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400",
                })