from django.db import models

class ContactMessage(models.Model):
    """
    Represents a contact message submitted by a user.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"