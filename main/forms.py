from django import forms
from .models import ShortenedURL

class URLForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(attrs={'placeholder': 'Enter your URL here'}),
        }
