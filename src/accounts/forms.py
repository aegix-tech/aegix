from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    """
    A form for registering a new user using the `CustomUser` model.

    This form extends Django's built-in `UserCreationForm` and only requires an email address by default.
    It also includes custom handling for the `usable_password` field if it exists.

    Attributes:
        Meta:
            model (CustomUser): The model associated with this form.
            fields (tuple[str, ...]): Specifies the fields to be used in the form. In this case, only the 'email' field is included.

    Methods:
        __init__(self, *args: Any, **kwargs: Any) -> None:
            Initializes the form and customizes the `usable_password` field widget to be hidden if it is present.
    """

    class Meta:
        model = CustomUser
        fields: tuple[str, ...] = ('email',)

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the form. If the `usable_password` field is present, its widget is set to be hidden.

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        if 'usable_password' in self.fields:
            self.fields['usable_password'].widget = forms.HiddenInput()

