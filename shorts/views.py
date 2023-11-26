from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Short
from .forms import ShortForm

@login_required
def short_list(request):
    shorts = Short.objects.all()
    return render(request, 'shorts/short_list.html', {'shorts': shorts})

@login_required
def short_detail(request, pk):
    short = get_object_or_404(Short, pk=pk)
    return render(request, 'shorts/short_detail.html', {'short': short})

@login_required
def short_create(request):
    if request.method == 'POST':
        form = ShortForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('short_list')
    else:
        form = ShortForm()
    return render(request, 'shorts/short_form.html', {'form': form})

@login_required
def short_update(request, pk):
    short = get_object_or_404(Short, pk=pk)
    if request.method == 'POST':
        form = ShortForm(request.POST, instance=short)
        if form.is_valid():
            form.save()
            return redirect('short_list')
    else:
        form = ShortForm(instance=short)
    return render(request, 'shorts/short_form.html', {'form': form, 'short': short})

@login_required
def short_delete(request, pk):
    short = get_object_or_404(Short, pk=pk)
    short.delete()
    return redirect('short_list')
