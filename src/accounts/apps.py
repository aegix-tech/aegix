from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the 'accounts' Django application.

    Attributes:
        default_auto_field (str): Specifies the default primary key field type to be used for models in the app.
            By default, it is set to 'django.db.models.BigAutoField'.
        name (str): The name of the application. In this case, it is 'accounts'.
    """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'accounts'
