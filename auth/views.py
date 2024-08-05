from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from auth.utils.sign_in import SignInHandler
from auth.utils.sign_up import SignUpHandler


@never_cache
@require_http_methods(["GET", "POST"])
def sign_in(request: HttpRequest) -> HttpResponse:
    """
    The sign in view

    Parameters
    ----------
    request : HttpRequest
        The request object

    Returns
    -------
    HttpResponse
        The rendered sign in page
    """

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST" and request.htmx:
        sign_in_handler = SignInHandler(
            request=request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        sign_in_handler.validate_data()

        if sign_in_handler.invalid:
            return render(
                request, "form-errors.html", {"errors": sign_in_handler.errors}
            )

        sign_in_handler.validate_user()

        if sign_in_handler.invalid:
            return render(
                request, "form-errors.html", {"errors": sign_in_handler.errors}
            )

        login(request, sign_in_handler.user)

        return HttpResponseClientRedirect("/")

    from_redirection = bool(request.GET.get("next"))

    return render(request, "auth/sign-in.html", {"from_redirection": from_redirection})


@never_cache
@require_http_methods(["GET", "POST"])
def sign_up(request: HttpRequest) -> HttpResponse:
    """
    The sign up view

    Parameters
    ----------
    request : HttpRequest
        The request object

    Returns
    -------
    HttpResponse
        The rendered sign up page
    """

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST" and request.htmx:
        sign_up_handler = SignUpHandler(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password"),
        )

        sign_up_handler.validate_data()

        if sign_up_handler.invalid:
            return render(
                request, "form-errors.html", {"errors": sign_up_handler.errors}
            )

        sign_up_handler.validate_user()

        if sign_up_handler.invalid:
            return render(
                request, "form-errors.html", {"errors": sign_up_handler.errors}
            )

        sign_up_handler.user.save()
        login(request, sign_up_handler.user)

        return HttpResponseClientRedirect("/")

    return render(request, "auth/sign-up.html")


@require_http_methods(["GET"])
def sign_out(request: HttpRequest) -> None:
    """
    The sign out endpoint

    Parameters
    ----------
    request : HttpRequest
        The request object
    """

    if request.htmx:
        logout(request)

        return HttpResponseClientRedirect("/sign-in")
