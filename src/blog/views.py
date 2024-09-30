from typing import Any, Optional, Union
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db.models import QuerySet

from .models import BlogPost, Author


class AuthorCreateView(CreateView):
    """View to create a new Author instance.

    Attributes:
        model (type[Author]): The model associated with the view.
        fields (Union[list[str], str]): The fields to be displayed in the form, or '__all__' to display all fields.
        template_name (str): The path to the template used for rendering.
        success_url (str): The URL to redirect to upon successful form submission.
    """
    model: type[Author] = Author
    fields = '__all__'
    template_name: str = 'blog/create_author.html'
    success_url: str = reverse_lazy('blog:list-author')


class AuthorListView(ListView):
    """View to list all Author instances.

    Attributes:
        model (type[Author]): The model associated with the view.
        template_name (str): The path to the template used for rendering.
        context_object_name (str): The name of the context variable representing the list of authors.
    """
    model: type[Author] = Author
    template_name: str = 'blog/list_author.html'
    context_object_name: str = 'authors'


class BlogHome(ListView):
    """View to list all blog posts.

    Attributes:
        model (type[BlogPost]): The model associated with the view.
        template_name (str): The path to the template used for rendering.
        context_object_name (str): The name of the context variable representing the blog posts.

    Methods:
        get_queryset: Filters blog posts based on whether the user is authenticated.
    """
    model: type[BlogPost] = BlogPost
    template_name: str = 'blog/blogpost_list.html'
    context_object_name: str = 'blog'

    def get_queryset(self) -> QuerySet[BlogPost]:
        """Return a filtered queryset of blog posts.

        If the user is authenticated, returns all blog posts. Otherwise, returns only the posts that are published.

        Returns:
            QuerySet[BlogPost]: A queryset of BlogPost instances.
        """
        queryset: QuerySet[BlogPost] = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(published=True)


class BlogPostCreate(CreateView):
    """View to create a new BlogPost instance.

    Attributes:
        model (type[BlogPost]): The model associated with the view.
        template_name (str): The path to the template used for rendering.
        fields (list[str]): The fields to be displayed in the form.
        success_url (str): The URL to redirect to upon successful form submission.
    """
    model: type[BlogPost] = BlogPost
    template_name: str = 'blog/blogpost_create.html'
    fields: list[str] = ['title', 'content', 'thumbnail']
    success_url: str = reverse_lazy('blog:home')


class BlogPostUpdate(UpdateView):
    """View to update an existing BlogPost instance.

    Attributes:
        model (type[BlogPost]): The model associated with the view.
        template_name (str): The path to the template used for rendering.
        fields (list[str]): The fields to be updated in the form.
        success_url (str): The URL to redirect to upon successful form submission.
    """
    model: type[BlogPost] = BlogPost
    template_name: str = 'blog/blogpost_edit.html'
    fields: list[str] = ['title', 'content', 'published']
    success_url: str = reverse_lazy('blog:home')


class BlogPostDetail(DetailView):
    """View to display details of a single BlogPost instance.

    Attributes:
        model (type[BlogPost]): The model associated with the view.
        template_name (str): The path to the template used for rendering.
        context_object_name (str): The name of the context variable representing the blog post.
    """
    model: type[BlogPost] = BlogPost
    template_name: str = 'blog/blogpost_detail.html'
    context_object_name: str = 'post'


class BlogPostDelete(DeleteView):
    """View to delete a BlogPost instance.

    Attributes:
        model (type[BlogPost]): The model associated with the view.
        template_name (str): The path to the template used for rendering.
        context_object_name (str): The name of the context variable representing the blog post.
        success_url (str): The URL to redirect to upon successful deletion.
    """
    model: type[BlogPost] = BlogPost
    template_name: str = 'blog/blogpost_confirm_delete.html'
    context_object_name: str = 'post'
    success_url: str = reverse_lazy('blog:home')
