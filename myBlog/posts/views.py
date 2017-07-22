import urllib

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Post
from .form import PostForm
import imghdr
from rest_framework import generics
from .serializers import PostSerializer
from django.contrib.auth import models
# Create your views here.


def post_list(request):
    query_set = Post.objects.all().order_by("-timestamp")

    return render(request, "list.html", {'object_list':query_set})


def post_detail(request, pk=None):
    instance = get_object_or_404(Post, id=pk)
    return render(request, "detail.html", {'instance': instance})


@login_required(login_url="/admin/login")
@permission_required(perm='posts.add_post', raise_exception=ValueError)
def post_create(request):
    # if not request.user.is_superuser or not request.user.is_staff:
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Unsuccessful")
    context = {
        'form': form
    }
    return render(request, "create.html", context)


def post_update(request, pk=None):
    if not request.user.is_superuser or not request.user.is_staff:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successful")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, "create.html", context)


class PostCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def post_delete(request, pk=None):
    instance = get_object_or_404(Post, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("post_list")


def upload(f):
    file = open(f.name, 'wb+')
    for chunk in f.chunks():
        file.write(chunk)

def upload_image(request):
    image = request.FILES
    if image:
        for item in image.getlist('pic'):
            upload(item)
        return HttpResponse("<p>Successful<p/>")
    #if image and imghdr.what(image['pic']) is not None:
        #upload(image['pic'])
        #return HttpResponse("<p>Successful<p/>")
    return render(request, "image.html", {})