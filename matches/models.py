from django.db import models


class Match(models.Model):
    """
    Match model
    """

    date = models.DateField()
    league = models.CharField(max_length=255)
    season = models.IntegerField()
    team1 = models.CharField(max_length=255)
    team2 = models.CharField(max_length=255)
    spi1 = models.FloatField()
    spi2 = models.FloatField()
    prob1 = models.FloatField()
    prob2 = models.FloatField()
    probtie = models.FloatField()
    proj_score1 = models.FloatField()
    proj_score2 = models.FloatField()
    score1 = models.IntegerField()
    score2 = models.IntegerField()

    class Meta:
        db_table = "matches"
