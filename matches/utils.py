from django.db.models import Max
from django.http import HttpRequest

from matches.models import Match


def generate_match_filters(request: HttpRequest) -> dict[str, str]:
    """
    Generate match filters.

    Parameters
    ----------
    request : HttpRequest
        The request object.

    Returns
    -------
    dict[str, str]
        The match filters.
    """

    filters = {}

    date = request.GET.get("date") or Match.objects.aggregate(Max("date"))["date__max"]
    league = request.GET.get("league")

    filters["date"] = date

    if league:
        filters["league"] = league

    return filters
