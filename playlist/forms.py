from django import forms
from .models import UserPlayList


class PlayListForm(forms.ModelForm):
    class Meta:
        model = UserPlayList
        fields = ['name', 'description', 'videos_qty']
