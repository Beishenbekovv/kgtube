from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import CommentForm


def videos(request):
    videos_list = Video.objects.all()
    context = {"videos_list": videos_list}
    return render(request, 'videos.html', context)

def video(request, id):
    # 7
    # SELECT * FROM video_video WHERE id = 7;
    video_object = Video.objects.get(id=id)
    context = {}
    if request.user.is_authenticated:
        video_view, created = VideoView.objects.get_or_create(
            user=request.user,
            video=video_object,
        )
        if request.method == 'POST':
            if "txt" in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False) # ещё нет записи в БД
                    comment.user = request.user
                    comment.video = video_object
                    comment.save() # сохраняем в БД
                    messages.success(request, 'Комментарий успешно добавлен.')
                else:
                    messages.error(request, 'Ошибка! Данные не валидны')
            elif "like" in request.POST:
                video_object.likes += 1
                video_object.save()
            elif "dislike" in request.POST:
                video_object.likes -= 1
                video_object.save()  
            # return redirect(video, id=video_object.id)
    context = {
        "video": video_object,
        "comment_form": CommentForm()

    }
    return render(request, 'video.html', context)

def video_add(request):
    if request.method == "GET":
        return render(request, 'video_add.html')
    elif request.method == "POST":
        name = request.POST["video_name"]
        video_file = request.FILES["video_file"]
        video_object = Video(
            name=name,
            file_path=video_file,
            author=request.user
        )
        # video_object.description = "hello world"
        # INSERT INTO ...
        video_object.save()
        return redirect(video, id=video_object.id)

def video_update(request, id):
    video_object = Video.objects.get(id=id)
    context = {"video": video_object}

    if request.method == "POST":
        name = request.POST["video_name"]
        video_object.name = name
        video_object.save()
        return redirect(video, id=video_object.id)

    return render(request, 'video_update.html', context)

def video_delete(request, id):
    video_object = Video.objects.get(id=id)
    video_object.delete()
    return redirect(videos)