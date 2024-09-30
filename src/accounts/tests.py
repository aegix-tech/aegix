import pytest
from django.test import Client
from django.urls import reverse
from accounts.forms import UserRegistrationForm
from accounts.models import CustomUser


@pytest.mark.django_db
class TestCustomUserModel:
    """
    Test suite for the CustomUser model.

    Methods:
        test_create_user: Tests the creation of a standard user and validates the email and password.
        test_create_superuser: Tests the creation of a superuser and checks the is_superuser and is_staff flags.
        test_user_string_representation: Tests that the string representation of the user is the email address.
    """

    def test_create_user(self) -> None:
        """
        Tests that a CustomUser can be created with an email and password.
        Verifies that the email is set correctly and the password is valid.
        """
        user: CustomUser = CustomUser.objects.create_user(email="test@example.com", password="testpass123")
        assert user.email == "test@example.com"
        assert user.check_password("testpass123")
        assert user.is_superuser is False
        assert user.is_staff is False

    def test_create_superuser(self) -> None:
        """
        Test the creation of a superuser with a specific email and password.

        This test verifies the following: The email is set correctly, the password is hashed and can be validated,
        the user has the superuser and staff privileges.
        """
        user: CustomUser = CustomUser.objects.create_superuser(email="admin@example.com", password="adminpass123")
        assert user.email == "admin@example.com"
        assert user.check_password("adminpass123")
        assert user.is_superuser is True
        assert user.is_staff is True


@pytest.mark.django_db
class TestUserRegistrationForm:
    """
    Test suite for the UserRegistrationForm.

    Methods:
        test_form_valid: Tests that the form is valid when provided with matching passwords and a valid email.
        test_form_invalid_password: Tests that the form is invalid when the passwords do not match.
    """

    def test_form_valid(self) -> None:
        """
        Tests that the UserRegistrationForm is valid with matching passwords and a valid email.
        Verifies that the user is successfully created with the provided email.
        """
        data: dict[str, str] = {'email': 'user@example.com', 'password1': 'testpass123', 'password2': 'testpass123'}
        form: UserRegistrationForm = UserRegistrationForm(data=data)
        assert form.is_valid() is True
        user: CustomUser = form.save()
        assert user.email == 'user@example.com'

    def test_form_invalid_password(self) -> None:
        """
        Tests that the UserRegistrationForm is invalid when the passwords do not match.
        Verifies that the form contains an error for the 'password2' field.
        """
        data: dict[str, str] = {'email': 'user@example.com', 'password1': 'testpass123', 'password2': 'differentpass'}
        form: UserRegistrationForm = UserRegistrationForm(data=data)
        assert form.is_valid() is False
        assert 'password2' in form.errors


@pytest.mark.django_db
class TestSignupView:
    """
    Test suite for the signup view.

    Methods:
        test_signup_view_get: Tests that the signup view renders correctly and includes the UserRegistrationForm in the context.
        test_signup_view_post_valid: Tests that a valid form submission redirects successfully and creates a new user.
        test_signup_view_post_invalid: Tests that an invalid form submission returns the form with errors.
    """

    def test_signup_view_get(self, client: Client) -> None:
        """
        Tests that the signup view returns a 200 status code and includes the UserRegistrationForm in the context when accessed via GET.

        Args:
            client (Client): Django test client to simulate a request.
        """
        url: str = reverse('accounts:signup')
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context
        assert isinstance(response.context['form'], UserRegistrationForm)

    def test_signup_view_post_valid(self, client: Client) -> None:
        """
        Tests that a valid form submission to the signup view redirects with a 302 status code and creates a new user.

        Args:
            client (Client): Django test client to simulate a request.
        """
        url: str = reverse('accounts:signup')
        data: dict[str, str] = {'email': 'user@example.com', 'password1': 'testpass123', 'password2': 'testpass123'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert CustomUser.objects.filter(email='user@example.com').exists()

    def test_signup_view_post_invalid(self, client: Client) -> None:
        """
        Tests that an invalid form submission to the signup view returns a 200 status code and includes errors in the form.

        Args:
            client (Client): Django test client to simulate a request.
        """
        url: str = reverse('accounts:signup')
        data: dict[str, str] = {'email': 'user@example.com', 'password1': 'testpass123', 'password2': 'differentpass'}
        response = client.post(url, data)
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors


@pytest.mark.django_db
class TestProfileView:
    """
    Test suite for the profile view.

    Methods:
        test_profile_view_accessible_by_logged_in_user: Tests that the profile view is accessible to logged-in users.
        test_profile_view_redirects_for_anonymous_user: Tests that the profile view redirects to the login page for anonymous users.
    """

    def test_profile_view_accessible_by_logged_in_user(self, client: Client) -> None:
        """
        Tests that the profile view returns a 200 status code for logged-in users.

        Args:
            client (Client): Django test client to simulate a request.
        """
        user: CustomUser = CustomUser.objects.create_user(email='user@example.com', password='testpass123')
        client.force_login(user)
        url: str = reverse('accounts:profile')
        response = client.get(url)
        assert response.status_code == 200

    def test_profile_view_redirects_for_anonymous_user(self, client: Client) -> None:
        """
        Tests that the profile view redirects to the login page with a 302 status code for anonymous users.

        Args:
            client (Client): Django test client to simulate a request.
        """
        url: str = reverse('accounts:profile')
        response = client.get(url)
        assert response.status_code == 302  # Redirect to login
