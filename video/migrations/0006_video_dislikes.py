# Generated by Django 4.2.7 on 2023-11-23 15:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0005_video_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='dislikes',
            field=models.ManyToManyField(related_name='disliked_videos', to=settings.AUTH_USER_MODEL),
        ),
    ]
