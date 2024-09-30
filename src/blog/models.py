from typing import Any
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.db import models
from django.urls import reverse


class Author(models.Model):
    """Model representing an author with a first name and last name."""

    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)

    def clean(self) -> None:
        """
        Validates that an Author with the same first and last name does not already exist.

        Raises:
            ValidationError: If an Author with the same firstname and lastname is found in the database.
        """
        if Author.objects.filter(firstname=self.firstname, lastname=self.lastname).exists():
            raise ValidationError(
                f'Un auteur avec le prénom "{self.firstname}" et le nom "{self.lastname}" existe déjà.'
            )

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Overrides the save method to perform validation before saving.

        Calls the `clean` method to ensure that the Author is unique.
        Then, calls the superclass's save method to store the object.
        """
        self.clean()
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Model representing a blog post with metadata, content, and an optional author."""

    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    title = models.CharField(max_length=255, unique=True, verbose_name='Titre')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True)
    last_updated: models.DateTimeField = models.DateTimeField(auto_now=True)
    created_on: models.DateField = models.DateField(blank=True, null=True)
    published: models.BooleanField = models.BooleanField(default=False, verbose_name='Publié')
    content = models.TextField(blank=True, verbose_name='Contenu')
    thumbnail = models.ImageField(blank=True, upload_to='mediablog')

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Article'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the save method to automatically generate a slug from the title if not provided.

        If the `slug` field is empty, it will be generated using the `slugify` function based on the title.
        Then, calls the superclass's save method to store the object.
        """
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    @property
    def author_or_default(self) -> str:
        return f'{self.author.firstname} {self.author.lastname}' if self.author else 'auteur inconnu'

    def get_blog_detail_absolute_url_with_slug(self) -> str:
        return reverse('blog:detail', kwargs={'slug': self.slug})
