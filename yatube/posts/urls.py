from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Просмотр постов группы
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    # Профайл пользователя
    path('profile/<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # Новая запись
    path('create/', views.post_create, name='post_create'),
    # Редактировать пост
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]
