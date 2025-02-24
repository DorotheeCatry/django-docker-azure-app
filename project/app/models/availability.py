from django.db import models

class Availability(models.Model):
    """
    Represents the availability of time slots for a specific date.
    """
    date = models.DateField(unique=True)
    time_slots = models.JSONField(default=list)

    def __str__(self):
        return f"{self.date} - {', '.join(self.time_slots)}"