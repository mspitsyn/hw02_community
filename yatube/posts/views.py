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
        'page_obj': page_obj
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
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
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
    author = post.author
    posts = Post.objects.filter(author=author)
    context = {
        'post': post,
        'author': author,
        'posts': posts
    }
    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'
    username = request.user.username
    form = PostForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        group = form.cleaned_data['group']
        new_post = Post(
            text=text,
            author=request.user,
            group=group
        )
        new_post.save()
        return redirect('posts:profile', username=username)
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
        context = {'form': form,
                   'is_edit': is_edit,
                   'post_id': post_id}
    return render(request, 'posts/create_post.html', context)
