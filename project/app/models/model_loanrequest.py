from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LoanRequest(models.Model):
    """
    Modèle pour les demandes de prêt.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_requests')
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)  # Dernière mise à jour
    
    # Attributs du prêt
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Montant du prêt
    term = models.IntegerField()  # Durée du prêt en mois
    
    # Attributs de la demande de prêt
    low_doc = models.CharField(max_length=1, choices=[('1', 'Yes'), ('0', 'No')])  # LowDoc = 1 ou 0
    rev_line_cr = models.CharField(max_length=1, choices=[('1', 'Yes'), ('0', 'No')])  # RevLineCr = 1 ou 0
    no_emp = models.FloatField()  # Nombre d'employés
    naics = models.CharField(max_length=2)  # Code NAICS
    new = models.CharField(max_length=1, choices=[('1', 'New'), ('0', 'Existing')])  # New = 1 ou 0
    franchise = models.CharField(max_length=1, choices=[('1', 'Franchise'), ('0', 'Non-Franchise')])  # Franchise = 1 ou 0

    # Attributs de localisation
    state = models.CharField(max_length=2)  # Abréviation de l'état
    rural = models.CharField(max_length=4, choices=[('0', 'Urban'), ('1', 'Rural'), ('None', 'Undefined')])  # Urban, Rural ou Undefined
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"LoanRequest #{self.id} - {self.status} - {self.amount}€ ({self.user.username})"
