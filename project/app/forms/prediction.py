from django import forms
from .models import UserProfile

class PredictChargesForm(forms.ModelForm):
    """
    Form for predicting insurance charges based on user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ["age", "height", "weight", "num_children", "smoker"]