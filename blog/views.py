from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Publicacion
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def listado(request):
    posts = Publicacion.objects.filter(fecha_creacion__lte = timezone.now()).order_by('fecha_creacion')
    return render(request, 'blog/listar.html', {'posts': posts})

def detalle(request, pk):
    post = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'blog/detalle.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            #post.fecha_creacion = timezone.now()
            post.save()
            return redirect('detalle', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            #post.fecha_creacion = timezone.now()
            post.save()
            return redirect('detalle', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Publicacion.objects.filter(fecha_creacion__isnull=True).order_by('fecha_creacion')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Publicacion, pk=pk)
    post.publicar()
    return redirect('detalle', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Publicacion, pk=pk)
    post.eliminar()
    return render(request, 'blog/listar.html')
