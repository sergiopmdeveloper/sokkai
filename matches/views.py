from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render


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

    return render(request, "matches/results.html")


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
