from django.db import models
from .user import UserProfile

class PredictionHistory(models.Model):
    """
    Represents a record of an insurance prediction for a user.
    """
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='insurance_predictions'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    num_children = models.PositiveIntegerField()
    smoker = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
    sex = models.CharField(max_length=10)
    predicted_charges = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Insurance Prediction"
        verbose_name_plural = "Insurance Predictions"
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]

    @property
    def bmi(self):
        """Preserve historical BMI calculation."""
        if self.height <= 0:
            0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self):
        return f"{self.user} prediction @ {self.timestamp:%Y-%m-%d}"