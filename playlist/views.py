from django.shortcuts import render, redirect
from .models import UserPlayList
from .forms import PlayListForm
from django.contrib.auth.decorators import login_required  

@login_required
def playlists(request):
    query_result = UserPlayList.objects.filter(owner=request.user) 

    context = {"objects_list": query_result}
    return render(request, 'playlists.html', context)

@login_required
def playlist_info(request, id):
    playlist_object = UserPlayList.objects.get(id=id, owner=request.user)  
    context = {"playlist_object": playlist_object}
    return render(request, "playlist_info.html", context)

@login_required
def playlist_add(request):
    if request.method == "POST":
        name = request.POST["playlist_name"]
        description = request.POST["description"]
        playlist_object = UserPlayList.objects.create(
            name=name,
            description=description,
            owner=request.user,  # Устанавливаем текущего пользователя как владельца
        )
        return redirect(playlist_info, id=playlist_object.id)
    
    return render(request, "playlist_add.html")


def playlist_df_add(request):
    context = {}
    if request.method == "POST":
        # код создания playlist 

        # создаём объект формы с значениями
        playlist_form = PlayListForm(request.POST)
        # проверка валидности
        if playlist_form.is_valid():
            # создаём запись в БД
            playlist_object = playlist_form.save()
            return redirect(playlist_info, id=playlist_object.id)
    
    playlist_form = PlayListForm()
    context["playlist_form"] = playlist_form
    return render(request, "playlist_df_add.html", context)
