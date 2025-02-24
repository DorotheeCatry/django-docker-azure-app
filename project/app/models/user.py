from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    Extends the default Django user model to include additional personal information.
    """
    class SmokerType(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'

    class RegionType(models.TextChoices):
        NORTHEAST = 'Northeast', 'Northeast'
        NORTHWEST = 'Northwest', 'Northwest'
        SOUTHEAST = 'Southeast', 'Southeast'
        SOUTHWEST = 'Southwest', 'Southwest'

    class SexType(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    age = models.PositiveIntegerField(default=25)
    weight = models.PositiveIntegerField(default=60, help_text="Weight in kilograms")
    height = models.PositiveIntegerField(default=170, help_text="Height in centimeters")
    num_children = models.PositiveIntegerField(default=0)
    smoker = models.CharField(max_length=10, choices=SmokerType.choices)
    region = models.CharField(max_length=10, choices=RegionType.choices)
    sex = models.CharField(max_length=10, choices=SexType.choices)

    @property
    def bmi(self):
        """Calculate BMI safely with zero division protection."""
        if self.height <= 0:
            0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self):
        return f"{self.username}"