import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


def test_sign_in_get_success(client: Client):
    """
    Tests the GET method of the sign in view and expects
    the response to be successful and the correct templates to be used
    """

    response = client.get(reverse("sign-in"))
    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "page.html" in templates
    assert "auth/sign-in.html" in templates


@pytest.mark.django_db
def test_sign_in_get_user_authenticated(client: Client):
    """
    Tests the GET method of the sign in view when the user is authenticated
    and expects the response to be a redirection
    """

    user = User.objects.create_user(username="username", password="password")

    client.force_login(user=user)
    response = client.get(reverse("sign-in"))

    assert response.status_code == 302


def test_sign_in_post_invalid_data(client: Client):
    """
    Tests the POST method of the sign in view with invalid data
    and expects the response to be successful and the correct templates to be used
    """

    response = client.post(reverse("sign-in"), data={}, HTTP_HX_REQUEST="true")
    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "form-errors.html" in templates


@pytest.mark.django_db
def test_sign_in_post_invalid_user(client: Client):
    """
    Tests the POST method of the sign in view with an invalid user
    and expects the response to be successful and the correct templates to be used
    """

    response = client.post(
        reverse("sign-in"),
        data={"username": "username", "password": "password"},
        HTTP_HX_REQUEST="true",
    )

    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "form-errors.html" in templates


@pytest.mark.django_db
def test_sign_in_post_success(client: Client):
    """
    Tests the POST method of the sign in view with valid data and user
    and expects the response to be successful and the user to be authenticated
    """

    user = User.objects.create_user(username="username", password="password")

    response = client.post(
        reverse("sign-in"),
        data={"username": "username", "password": "password"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert client.session["_auth_user_id"] == str(user.id)


def test_sign_up_get_success(client: Client):
    """
    Tests the GET method of the sign up view and expects
    the response to be successful and the correct templates to be used
    """

    response = client.get(reverse("sign-up"))
    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "page.html" in templates
    assert "auth/sign-up.html" in templates


@pytest.mark.django_db
def test_sign_up_get_user_authenticated(client: Client):
    """
    Tests the GET method of the sign up view when the user is authenticated
    and expects the response to be a redirection
    """

    user = User.objects.create_user(username="username", password="password")

    client.force_login(user=user)
    response = client.get(reverse("sign-up"))

    assert response.status_code == 302


def test_sign_up_post_invalid_data(client: Client):
    """
    Tests the POST method of the sign up view with invalid data
    and expects the response to be successful and the correct templates to be used
    """

    response = client.post(reverse("sign-up"), data={}, HTTP_HX_REQUEST="true")
    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "form-errors.html" in templates


@pytest.mark.django_db
def test_sign_up_post_invalid_user(client: Client):
    """
    Tests the POST method of the sign up view with an invalid user
    and expects the response to be successful and the correct templates to be used
    """

    User.objects.create_user(username="username")

    response = client.post(
        reverse("sign-up"),
        data={
            "username": "username",
            "email": "username@email.com",
            "password": "password152",
        },
        HTTP_HX_REQUEST="true",
    )

    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "form-errors.html" in templates


@pytest.mark.django_db
def test_sign_up_post_success(client: Client):
    """
    Tests the POST method of the sign up view with valid data and user
    and expects the response to be successful and the user to be authenticated
    """

    response = client.post(
        reverse("sign-up"),
        data={
            "username": "username",
            "email": "username@email.com",
            "password": "password152",
        },
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert client.session["_auth_user_id"]


@pytest.mark.django_db
def test_sign_out_endpoint(client: Client):
    """
    Tests the GET method of the sign out endpoint
    and expects the user to be signed out
    """

    user = User.objects.create_user(username="username", password="password")

    client.force_login(user=user)
    response = client.get(reverse("sign-out"), HTTP_HX_REQUEST="true")

    assert response.status_code == 200
    assert not client.session.get("_auth_user_id")
