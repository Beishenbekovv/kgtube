from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['txt']



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name']
