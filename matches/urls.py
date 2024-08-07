from django.urls import path

from matches.views import match_results, matches

urlpatterns = [
    path("results", match_results, name="match-results"),
    path("", matches, name="matches"),
]
