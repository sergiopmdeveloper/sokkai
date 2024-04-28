from django.urls import path

from . import views

urlpatterns = [
    path("results", views.results, name="match_results"),
]
