from typing import Optional, Any, Union

from django.contrib import admin
from django.http import HttpRequest

from .models import BlogPost

typing_fieldset = Union[list[tuple[Optional[Any], Any]], tuple[tuple[Optional[Any], Any], ...]]


class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface configuration for the BlogPost model.

    This class customizes the admin interface for the `BlogPost` model,
    including which fields are displayed, editable, and organized into fieldsets.

    Attributes:
        list_display (tuple[str, ...]): Fields to display in the list view.
        list_editable (tuple[str, ...]): Fields that can be edited directly in the list view.
        fieldsets (tuple[str, dict]): Configuration of fields grouped by sections in the form view.
        add_fieldsets (list[tuple[str, dict]]): Configuration of fields grouped by sections
            when creating a new `BlogPost`.
    """
    list_display: tuple[str, ...] = ('title', 'published', 'created_on', 'last_updated',)
    list_editable: tuple[str, ...] = ('published',)
    fieldsets: list[tuple[Optional[Any], Any]] = [
        ('Informations Générales', {'fields': ('title', 'slug', 'author')}),
        ('SEO', {'fields': ('meta_description', 'keywords')}),
        ('Contenu', {'fields': ('content', 'thumbnail')}),
        ('Publication', {'fields': ('published', 'created_on')}),
    ]

    add_fieldsets: list[tuple[Optional[Any], Any]] = [
        ('Nouvel objet - Informations Générales', {'fields': ('title', 'slug', 'author')}),
        ('Nouvel objet - SEO', {'fields': ('meta_description', 'keywords')}),
        ('Nouvel objet - Contenu', {'fields': ('content', 'thumbnail')}),
        ('Nouvel objet - Publication', {'fields': ('published', 'created_on')}),
    ]

    def get_fieldsets(self, request: HttpRequest, obj: Optional[BlogPost] = None) -> typing_fieldset:
        """Return the fieldsets to use in the form view.

        This method determines which fieldsets to display depending on whether
        a `BlogPost` instance is being added or edited.

        Args:
            request (HttpRequest): The current request object.
            obj (Optional[BlogPost]): The instance of `BlogPost` being edited,
                or `None` if a new instance is being created.

        Returns:
            list[Tuple[str, dict]]: The list of fieldsets to display.
        """
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


admin.site.register(BlogPost, BlogPostAdmin)
