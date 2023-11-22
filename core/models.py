from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    channel_name = models.CharField(
        max_length=100,
        verbose_name="Название канала",
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.PROTECT,
        related_name="profile",
        verbose_name="Владелец"
    )
    subscribers = models.ManyToManyField(
        to=User,
        related_name="subscriptions",
        verbose_name="Подписки",
        blank=True
    )
    photo = models.ImageField(
        null=True, blank=True,
        default="/static/img/avatar.jpg",
        upload_to="profile_photo/"
    )
    created_by = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
