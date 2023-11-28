from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.db.models import Q
from video.models import Video
from .models import Profile
from .forms import *


def registration(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.method == "POST":
        registration_form = UserCreateForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(request.POST["password"])
            new_user.save()
            Profile.objects.create(
                channel_name=new_user.username,
                user=new_user
            )
            messages.success(request, "Вы успешно прошли регистрацию")

    context["registration_form"] = UserCreateForm()
    return render(request, "user/registration.html", context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("home")
    

    if request.method == "POST":
        auth_form = UserAuthForm(request.POST)
        if auth_form.is_valid():
            # индентификация
            user_object = authenticate(
                username=request.POST["username"],
                password=request.POST.get("password")
            )
            # авторизация
            if user_object:
                login(request, user_object)
                messages.success(request, "Успешно авторизовано!")
            else:
                messages.error(request, "Неверный логин или пароль")
        else:
            # print(auth_form.errors)
            messages.error(request, auth_form.errors)  
            
    return render(
        request,
        "user/sign_in.html",
        {"auth_form": UserAuthForm()}
    )

def sign_out(request):
    logout(request)
    return redirect("home")

# Create your views here.
def homepage(request):
    # return HttpResponse("hello world")
    return render(request, "home.html")

def about_view(request):
    return render(request, 'about.html')

def search(request):
    key_word = request.GET["key_word"]
    # SELECT * FROM Video WHERE name LIKE '%key_word%'
    # videos_query = Video.objects.filter(name__contains=key_word)
    # videos_query = Video.objects.filter(description__contains=key_word)
    videos_query = Video.objects.filter(
        Q(name__contains=key_word) |
        Q(author__username__contains=key_word) |
        Q(description__contains=key_word),
        is_published=True
    )
    context = {"videos_list": videos_query}
    return render(request, "videos.html", context)

def profile_create(request):
    context = {}
    if request.method == "POST":
        profile_form = ProfileForm(
            data=request.POST,
            files=request.FILES
        )
        if profile_form.is_valid():
            profile_object = profile_form.save(commit=False)
            profile_object.user = request.user
            profile_object.save()
            messages.success(request, "Профиль и канал успешно созданы")
            return redirect(f'/profile/{profile_object.id}/')
        else:
            messages.error(request, "Ошибка при создании профиля")

    profile_form = ProfileForm()
    context["profile_form"] = profile_form
    return render(
        request=request,
        template_name="profile_create.html",
        context=context
    )

def profile_detail(request, id):
    context = {}
    profile_object = Profile.objects.get(id=id)
    context["profile_object"] = profile_object

    # subscribers_qty = profile_object.subscribers.count()
    subscribers_qty = User.objects.filter(subscriptions=profile_object).count()
    context["subscribers_qty"] = subscribers_qty

    # [video_1, video_2, ...] видео этого пользователя
    videos_list = profile_object.user.video_set.all()
    # videos_list = Video.objects.filter(author=profile_object.user)
    context["videos_list"] = videos_list 


    return render(
        request,
        'profile.html',
        context
    )

def profile_update(request, id):
    context = {}
    profile_object = Profile.objects.get(id=id)
    if request.user == profile_object.user:
        if request.method == "POST":
            profile_form = ProfileForm(
                instance=profile_object,
                data=request.POST,
                files=request.FILES,
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профиль успешно обновлён!")
                return redirect(profile_detail, id=profile_object.id)

        profile_form = ProfileForm(instance=profile_object)
        context["profile_form"] = profile_form
        return render(request, "profile_update.html", context)
    else:
        return HttpResponse("Нет доступа")


class ProfileUpdate(View):
    # read
    def get(self, request, *args, **kwargs):
        context = {}
        profile_object = Profile.objects.get(id=kwargs.get("pk"))
        profile_form = ProfileForm(instance=profile_object)
        context["profile_form"] = profile_form
        return render(request, "profile_update.html", context)
    
    # update
    def post(self, request, *args, **kwargs):
        profile_object = Profile.objects.get(id=kwargs.get("pk"))
        if request.user == profile_object.user:
            profile_form = ProfileForm(
                instance=profile_object,
                data=request.POST,
                files=request.FILES,
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профиль успешно обновлён!")
                return redirect("profile-update-cbv", pk=profile_object.id)
            else:
                return HttpResponse("Данные не валидны", status=400)
        else:
            return HttpResponse("Нет доступа", status=403)




def profile_delete(request, id):
    context = {}
    if request.user == profile_object.user:
        profile_object = Profile.objects.get(id=id)
        context["profile_object"] = profile_object

        if request.method == "POST":
            profile_object.delete()
            return redirect("home")
        return render(request, "profile_delete.html", context)
    else:
        return HttpResponse("Нет доступа")


def subscriber_add(request,id):
    if request.method == "POST":
        profile_object = Profile.objects.get(id=id)
        profile_object.subscribers.add(request.user)
        profile_object.save()
        return redirect(profile_detail, id=profile_object.id)

def subscriber_remove(request,id):
    if request.method == "POST":
        profile_object = Profile.objects.get(id=id)
        profile_object.subscribers.remove(request.user)
        profile_object.save()
        return redirect(profile_detail, id=profile_object.id)