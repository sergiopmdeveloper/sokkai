from django.core.management.base import CommandError


class DownloadError(CommandError):
    """
    Exception raised when an error
    occurs downloading matches data
    """

    pass


class FieldsNotFound(CommandError):
    """
    Exception raised when one or multiple
    fields are not found in the matches data
    """

    pass
