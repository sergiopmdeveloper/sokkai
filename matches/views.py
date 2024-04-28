from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from matches.models import Match
from matches.utils import generate_match_filters


@require_http_methods(["GET"])
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

    filters = generate_match_filters(request=request)

    matches = Match.objects.filter(**filters)

    return render(request, "matches/results.html", {"matches": matches})
