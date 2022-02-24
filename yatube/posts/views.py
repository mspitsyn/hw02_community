from django.shortcuts import render, get_object_or_404

from .models import Post, Group


def index(request):
    TEN_POSTS = 10
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:TEN_POSTS]
    title = 'Главная страница'
    text = 'Последние обновления на сайте'
    context = {
        'posts': posts,
        'title': title,
        'text': text,
    }
    return render(request, template, context)


def group_posts(request, slug):
    TEN_POSTS = 10
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:TEN_POSTS]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
