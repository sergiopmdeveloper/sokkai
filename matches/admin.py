from django.contrib import admin

from matches.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """
    Match admin
    """

    list_display = ("date", "team1", "team2", "score1", "score2")
