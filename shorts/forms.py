from django import forms
from .models import Short

class ShortForm(forms.ModelForm):
    class Meta:
        model = Short
        fields = ['title', 'description']
