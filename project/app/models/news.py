from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    """
    Model for news articles published on the homepage.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')

    def __str__(self):
        return self.title
    
    
