from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User

LIMIT_POSTS = 10


@login_required
def index(request):
    template = 'posts/index.html'
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    paginator = Paginator(posts_list, LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts_list': posts_list,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'
    username = request.user.username
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('posts:profile', username=username)
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    username = request.user.username
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:profile', username=username)
    else:
        form = PostForm(instance=post)
        context = {
            'is_edit': True,
            'post': post,
            'form': form
        }
        return render(request, template, context)
