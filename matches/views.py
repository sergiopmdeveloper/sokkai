from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from matches.constants import ALL_LEAGUES, MATCH_RESULTS_DEFAULT_DATE
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

    date = request.GET.get("date") or MATCH_RESULTS_DEFAULT_DATE
    league = request.GET.get("league") or ALL_LEAGUES

    matches = Match.objects.filter(**generate_match_filters(date=date, league=league))

    unique_leagues = list(Match.objects.values_list("league", flat=True).distinct())
    unique_leagues.sort()
    unique_leagues.insert(0, ALL_LEAGUES)

    return render(
        request,
        "matches/results.html",
        {
            "matches": matches,
            "unique_leagues": unique_leagues,
            "selected_date": date,
            "selected_league": league,
        },
    )
