from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configuration class for the blog application.

    This class configures the 'blog' application within the Django project. It specifies
    the default field type for automatically created primary keys as `BigAutoField`.

    Attributes:
        default_auto_field (str): The type of auto-created primary key fields.
        name (str): The name of the application.
    """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'blog'
