from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from matches.models import Match


@login_required(login_url="sign-in")
def match_results(request: HttpRequest) -> HttpResponse:
    """
    The match results view

    Parameters
    ----------
    request : HttpRequest
        The request object

    Returns
    -------
    HttpResponse
        The rendered match results page
    """

    match_results = Match.objects.filter(score1__isnull=False, score2__isnull=False)

    paginator = Paginator(match_results, 20)
    page = request.GET.get("page", 1)

    match_results = paginator.get_page(page)

    return render(request, "matches/results.html", {"matches": match_results})


def matches(_: HttpRequest) -> HttpResponseRedirect:
    """
    Redirects to the match results page

    Parameters
    ----------
    _ : HttpRequest
        The request object, not used

    Returns
    -------
    HttpResponseRedirect
        The redirect response
    """

    return redirect("match-results")
