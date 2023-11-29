import factory
from django.contrib.auth.models import User
from .models import *
from core.models import Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'test_user_1'


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
    channel_name = 'test channel'
    user = factory.SubFactory(UserFactory)


class VideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Video
    
    file_path = factory.django.FileField(file_path="/static/video/test_video.mp4") 
    name = factory.Sequence(lambda n: f"Test video {n}")
    author = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    video = factory.SubFactory(VideoFactory)
    txt = factory.Sequence(lambda n: f"comment number {n}") # comment number 0, comment number 1 ...