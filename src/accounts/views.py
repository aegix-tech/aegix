from typing import Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from accounts.forms import UserRegistrationForm


class SignupView(FormView):
    """
    Handles user signup by displaying a registration form and processing the form submission.

    Attributes:
        template_name (str): The path to the template used to render the signup form.
        form_class (Type[UserRegistrationForm]): The form class used for user registration, it's a class, not an instance.
        success_url (str): The URL to redirect to upon successful form submission.

    Methods:
        form_valid(form): Processes a valid form submission by saving the user data and redirecting to the success URL.
    """
    template_name: str = "registration/signup.html"
    form_class: Type[UserRegistrationForm] = UserRegistrationForm
    success_url: str = reverse_lazy('accounts:confirm')

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        """
        Saves the form data and redirects the user to the success URL.

        Args:
            form (UserRegistrationForm): The form instance containing the validated data.

        Returns:
            HttpResponse: The HTTP response redirecting the user to the success URL.
        """
        form.save()
        return super().form_valid(form)


class ConfirmView(TemplateView):
    """
    Displays a confirmation page after successful user signup.

    Attributes:
        template_name (str): The path to the template used to render the confirmation page.
    """
    template_name: str = "registration/confirm.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Displays the user's profile page.

    This view requires the user to be logged in.

    Attributes:
        template_name (str): The path to the template used to render the profile page.
    """
    template_name: str = 'registration/profile.html'
