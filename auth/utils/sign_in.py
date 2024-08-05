from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest

from auth.utils.abstract_auth import AbstractAuth


class SignInHandler(AbstractAuth):
    """
    The sign in handler

    Attributes
    ----------
    request : HttpRequest
        The request object
    username : str
        The username
    password : str
        The password
    errors : list[str]
        The list of errors
    user : Optional[User]
        The user

    Properties
    ----------
    invalid : bool
        True if there are errors, False otherwise

    Methods
    -------
    validate_data()
        Validates the data
    validate_user()
        Validates the user
    """

    def __init__(self, request: HttpRequest, username: str, password: str) -> None:
        """
        Initializes the sign in handler

        Parameters
        ----------
        request : HttpRequest
            The request object
        username : str
            The username
        password : str
            The password
        """

        self.request = request
        self.username = username
        self.password = password
        self.errors: list[str] = []
        self.user: Optional[User] = None

    @property
    def invalid(self) -> bool:
        """
        True if there are errors, False otherwise
        """

        return len(self.errors) > 0

    def validate_data(self) -> None:
        """
        Validates the data
        """

        if not self.username:
            self.errors.append("Username is required.")

        if not self.password:
            self.errors.append("Password is required.")

    def validate_user(self) -> None:
        """
        Validates the user
        """

        self.user = authenticate(
            self.request, username=self.username, password=self.password
        )

        if not self.user:
            self.errors.append("Invalid credentials.")
