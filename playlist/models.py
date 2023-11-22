from django.db import models
from django.contrib.auth.models import User


class UserPlayList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    videos_qty = models.IntegerField(default=0)
    views_qty = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name
