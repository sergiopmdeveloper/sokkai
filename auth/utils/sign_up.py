from typing import Optional

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from auth.utils.abstract_auth import AbstractAuth


class SignUpHandler(AbstractAuth):
    """
    The sign up handler

    Attributes
    ----------
    username : str
        The username
    email : str
        The email
    password : str
        The password
    errors : list[str]
        The list of errors
    user : Optional[User]
        The user
    """

    def __init__(self, username: str, email: str, password: str) -> None:
        """
        Initializes the sign up handler

        Parameters
        ----------
        username : str
            The username
        email : str
            The email
        password : str
            The password
        """

        self.username = username
        self.email = email
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

        if not self.email:
            self.errors.append("Email is required.")

        if not self.password:
            self.errors.append("Password is required.")

    def validate_user(self) -> None:
        """
        Validates the user
        """

        user = User(username=self.username, email=self.email, password=self.password)

        try:
            user.full_clean()
        except ValidationError as e:
            self.errors.extend(e.messages)

        try:
            validate_password(self.password)
        except ValidationError as e:
            self.errors.append(list(e.messages)[0])

        if not self.errors:
            self.user = user
