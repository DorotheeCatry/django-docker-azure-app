from django import forms
from django.forms import DateInput
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    """
    Form for creating or updating an appointment.
    """
    class Meta:
        model = Appointment
        fields = ['reason', 'date', 'time']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control w-full bg-gray-100 rounded-md p-2'}),
        }

    def clean_time(self):
        """
        Validates the time field to ensure it follows the HH:MM format.
        """
        time = self.cleaned_data.get('time')
        try:
            if not time:
                raise forms.ValidationError("This field is required.")
            hour, minute = map(int, time.split(":"))
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise forms.ValidationError("Enter a valid time in HH:MM format.")
        except (ValueError, TypeError):
            raise forms.ValidationError("Time should be in HH:MM format.")
        return time