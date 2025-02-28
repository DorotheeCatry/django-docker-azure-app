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

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    token = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} ({self.role})"



