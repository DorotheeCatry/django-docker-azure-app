from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    Modèle utilisateur personnalisé pour gérer les clients et les conseillers bancaires.
    """
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('advisor', 'Advisor'),
    ]

    # Supprimer la relation OneToOneField qui crée une redondance
    # Le champ user est déjà fourni par AbstractUser, donc on n'a pas besoin de OneToOneField
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    
    # Référence à un conseiller pour le client
    advisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='clients')

    #token = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} ({self.role})"

