from django import forms
from app.models import LoanRequest
from django.core.exceptions import ValidationError


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


    def clean(self):

        cleaned_data = super().clean()  

        amount = cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise ValidationError("Le montant doit être supérieur à 0.")


        term = cleaned_data.get("term")
        if term is not None and term <= 0:
            raise ValidationError("La durée doit être supérieure à 0.")


        no_emp = cleaned_data.get("no_emp")
        if no_emp is not None and no_emp < 0:
            raise ValidationError("Le nombre d'employés ne peut pas être négatif.")


        naics = cleaned_data.get("naics")
        if naics is not None and (not str(naics).isdigit() or len(str(naics)) != 2 ):
            raise ValidationError("Le code NAICS doit être un nombre à 2 chiffres.")


        state = cleaned_data.get("state")
        if state is not None and (not state.isalpha() or len(state) != 2):
            raise ValidationError("Le code d'État doit être composé de 2 lettres.")

        valid_choices = {
            "low_doc": ['Y', 'N'],
            "rev_line_cr": ['1', '0'],
            "new": ['1', '0'],
            "franchise": ['1', '0'],
            "rural": ['0', '1', 'None'],
        }

        for field, valid_values in valid_choices.items():
            value = cleaned_data.get(field)
            if value is not None and value not in valid_values:
                raise ValidationError[field] (f"Valeur invalide pour {field}.")


        return cleaned_data
