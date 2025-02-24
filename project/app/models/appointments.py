from django.db import models
from django.conf import settings
from datetime import date

class Appointment(models.Model):
    """
    Represents an appointment made by a user.
    """
    REASON_CHOICES = [
        ("Consultation", "Consultation"),
        ("Insurance Claim", "Insurance Claim"),
        ("Policy Inquiry", "Policy Inquiry"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    date = models.DateField(default=date(2025, 2, 3))
    time = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.reason} on {self.date} at {self.time}"