from django.shortcuts import render, get_object_or_404

from .models import Post, Group


def index(request):
    LIMIT_POSTS = 10
    template = 'posts/index.html'
    posts = Post.objects.all()[:LIMIT_POSTS]
    context = {
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    LIMIT_POSTS = 10
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:LIMIT_POSTS]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
