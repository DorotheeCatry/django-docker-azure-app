from django import forms
from app.models import News
from django.contrib.auth.models import User
class NewsForm(forms.ModelForm):
    """
    Formulaire pour soumettre un article d'actualité.
    """
    class Meta:
        model = News
        fields = ["title", "content", "author"]
    
    title = forms.CharField(max_length=255, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    author = forms.ModelChoiceField(queryset=User.objects.all(), required=True)