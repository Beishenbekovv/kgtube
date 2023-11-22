from django.db import models
from django.contrib.auth.models import User
from playlist.models import UserPlayList

# Create your models here.
class Video(models.Model):
    file_path = models.FileField(upload_to="video/") # путь к видео файлу
    name = models.CharField(max_length=60) # varchar
    likes = models.IntegerField(default=0) # int
    description = models.TextField(null=True) # text # blank = False
    is_published = models.BooleanField(default=True) # boolean
    playlist = models.ForeignKey(
        to=UserPlayList,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    txt = models.TextField(verbose_name="Текст комментария")
    video = models.ForeignKey(
        to=Video,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    created_by = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.txt[:10]


class VideoView(models.Model):
    video = models.ForeignKey(
        to=Video,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    created_by = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"
        unique_together = [["video", "user"]]
