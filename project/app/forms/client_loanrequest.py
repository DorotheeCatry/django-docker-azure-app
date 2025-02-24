from django import forms
from app.models import LoanRequest


class LoanRequestForm(forms.ModelForm):
    """
    Formulaire pour les demandes de prêt.
    """
    class Meta:
        model = LoanRequest
        fields = [
            'amount', 'term', 'low_doc', 'rev_line_cr', 'no_emp',
            'naics', 'new', 'franchise', 'state', 'rural'
        ]
        widgets = {
            'low_doc': forms.Select(choices=[('Y', 'Yes'), ('N', 'No')]),
            'rev_line_cr': forms.Select(choices=[('1', 'Yes'), ('0', 'No')]),
            'new': forms.Select(choices=[('1', 'New'), ('0', 'Existing')]),
            'franchise': forms.Select(choices=[('1', 'Franchise'), ('0', 'Non-Franchise')]),
            'rural': forms.Select(choices=[('0', 'Urban'), ('1', 'Rural'), ('None', 'Undefined')]),
        }
