import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from typing import Any

from blog.models import Author, BlogPost


@pytest.mark.django_db
class TestAuthorModel:
    """Test suite for the Author model."""

    def test_author_duplicate(self) -> None:
        """Test that creating an Author with duplicate firstname and lastname raises a ValidationError.

        This test ensures that if an Author with the same firstname and lastname
        already exists, attempting to save another Author with the same data
        raises a ValidationError.

        Raises:
            ValidationError: If an author with the same firstname and lastname is created.
        """
        Author.objects.create(firstname='John', lastname='Doe')

        author: Author = Author(firstname='John', lastname='Doe')
        with pytest.raises(ValidationError) as excinfo:
            author.save()

        assert str(excinfo.value) == "['Un auteur avec le prénom \"John\" et le nom \"Doe\" existe déjà.']"


@pytest.mark.django_db
class TestBlogPost:
    """Test suite for the BlogPost model."""

    def test_author_or_default(self) -> None:
        """Test the `author_or_default` property of the BlogPost model.

        This test ensures that the `author_or_default` property returns the author's
        full name if an author exists, otherwise a default value.
        """
        Author.objects.create(firstname='John', lastname='Doe')
        post: BlogPost = BlogPost(title='test', author=Author.objects.get(pk=1))
        assert post.author_or_default == 'John Doe'

    def test_get_blog_detail_absolute_url_with_slug(self) -> None:
        """Test the `get_absolute_url` method of the BlogPost model.

        This test ensures that the method correctly generates the absolute URL
        for a blog post based on its slug.
        """
        post: BlogPost = BlogPost.objects.create(title='Mon nouvel article')
        expected_url: str = reverse('blog:detail', kwargs={'slug': 'mon-nouvel-article'})
        assert post.get_blog_detail_absolute_url_with_slug() == expected_url
