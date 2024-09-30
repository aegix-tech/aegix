from django.urls import path, URLPattern
from .views import (
    BlogHome, BlogPostCreate, BlogPostUpdate, BlogPostDetail,
    BlogPostDelete, AuthorCreateView, AuthorListView
)
from django.contrib.auth.decorators import login_required

app_name: str = "blog"

urlpatterns: list[URLPattern] = [
    path('', BlogHome.as_view(), name='home'),
    path('create-author/', login_required(AuthorCreateView.as_view()), name='create-author'),
    path('list-author/', login_required(AuthorListView.as_view()), name='list-author'),
    path('create/', login_required(BlogPostCreate.as_view()), name='create'),
    path('<str:slug>/', BlogPostDetail.as_view(), name='detail'),
    path('edit/<str:slug>', login_required(BlogPostUpdate.as_view()), name='edit'),
    path('delete/<str:slug>', login_required(BlogPostDelete.as_view()), name='delete'),
]

