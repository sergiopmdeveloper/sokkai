from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def results(request: HttpRequest) -> HttpResponse:
    """
    Render the results page.

    Parameters
    ----------
    request : HttpRequest
        The request object.

    Returns
    -------
    HttpResponse
        The results page.
    """

    return render(request, "matches/results.html")
