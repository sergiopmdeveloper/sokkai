import pytest
from django.contrib.auth.models import User
from django.test import Client

from auth.utils.sign_in import SignInHandler
from auth.utils.sign_up import SignUpHandler


def test_sign_in_handler_initialization(client: Client):
    """
    Tests the initialization of the sign in handler
    and expects the attributes to be set correctly
    """

    sign_in_handler = SignInHandler(
        request=client.request,
        username="username",
        password="password",
    )

    assert sign_in_handler.request is not None
    assert sign_in_handler.username == "username"
    assert sign_in_handler.password == "password"
    assert sign_in_handler.errors == []
    assert sign_in_handler.user is None


@pytest.mark.parametrize(
    "username, password, errors, invalid",
    [
        ("", "", ["Username is required.", "Password is required."], True),
        ("username", "password", [], False),
    ],
)
def test_sign_in_handler_validate_data(
    client: Client, username: str, password: str, errors: list[str], invalid: bool
):
    """
    Tests the validate_data method of the sign in handler
    and expects the errors and invalid attributes to be set correctly
    """

    sign_in_handler = SignInHandler(
        request=client.request,
        username=username,
        password=password,
    )

    sign_in_handler.validate_data()

    assert sign_in_handler.errors == errors
    assert sign_in_handler.invalid == invalid


@pytest.mark.django_db
def test_sign_in_handler_validate_user_invalid_credentials(client: Client):
    """
    Tests the validate_user method of the sign in handler with invalid credentials
    and expects the user to be None and the errors to be set correctly
    """

    sign_in_handler = SignInHandler(
        request=client.request,
        username="username",
        password="password",
    )

    sign_in_handler.validate_user()

    assert not sign_in_handler.user
    assert sign_in_handler.errors == ["Invalid credentials."]


@pytest.mark.django_db
def test_sign_in_handler_validate_user_valid_credentials(client: Client):
    """
    Tests the validate_user method of the sign in handler with valid credentials
    and expects the user to be set correctly and the errors to be empty
    """

    user = User.objects.create_user(username="username", password="password")

    sign_in_handler = SignInHandler(
        request=client.request,
        username="username",
        password="password",
    )

    sign_in_handler.validate_user()

    assert sign_in_handler.user == user
    assert sign_in_handler.errors == []


def test_sign_up_handler_initialization():
    """
    Tests the initialization of the sign up handler
    and expects the attributes to be set correctly
    """

    sign_up_handler = SignUpHandler(
        username="username",
        email="email",
        password="password",
    )

    assert sign_up_handler.username == "username"
    assert sign_up_handler.email == "email"
    assert sign_up_handler.password == "password"
    assert sign_up_handler.errors == []
    assert sign_up_handler.user is None


@pytest.mark.parametrize(
    "username, email, password, errors, invalid",
    [
        (
            "",
            "",
            "",
            ["Username is required.", "Email is required.", "Password is required."],
            True,
        ),
        ("username", "email", "password", [], False),
    ],
)
def test_sign_up_handler_validate_data(
    username: str,
    email: str,
    password: str,
    errors: list[str],
    invalid: bool,
):
    """
    Tests the validate_data method of the sign up handler
    and expects the errors and invalid attributes to be set correctly
    """

    sign_up_handler = SignUpHandler(
        username=username,
        email=email,
        password=password,
    )

    sign_up_handler.validate_data()

    assert sign_up_handler.errors == errors
    assert sign_up_handler.invalid == invalid


@pytest.mark.django_db
def test_sign_up_handler_validate_user_invalid_credentials():
    """
    Tests the validate_user method of the sign up handler with invalid credentials
    and expects the errors and invalid attributes to be set correctly
    """

    User.objects.create_user(username="username")

    sign_up_handler = SignUpHandler(
        username="username",
        email="email",
        password="pass",
    )

    sign_up_handler.validate_user()

    assert sign_up_handler.errors == [
        "Enter a valid email address.",
        "A user with that username already exists.",
        "This password is too short. It must contain at least 8 characters.",
    ]

    assert sign_up_handler.invalid


@pytest.mark.django_db
def test_sign_up_handler_validate_user_valid_credentials():
    """
    Tests the validate_user method of the sign in handler with valid credentials
    and expects the user to be set correctly and the errors to be empty
    """

    sign_up_handler = SignUpHandler(
        username="username",
        email="username@email.com",
        password="password152",
    )

    sign_up_handler.validate_user()

    assert sign_up_handler.user
    assert sign_up_handler.errors == []
