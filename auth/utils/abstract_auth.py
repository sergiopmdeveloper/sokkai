from abc import ABC, abstractmethod


class AbstractAuth(ABC):
    """
    The abstract auth class
    """

    @abstractmethod
    def validate_data(self) -> None:
        """
        Validates the data
        """

    @abstractmethod
    def validate_user(self) -> None:
        """
        Validates the user
        """
