from django.db import models


class Match(models.Model):
    """
    Match model
    """

    season = models.CharField(max_length=50)
    date = models.DateField()
    league = models.CharField(max_length=50)
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    spi1 = models.FloatField()
    spi2 = models.FloatField()
    prob1 = models.FloatField()
    prob2 = models.FloatField()
    probtie = models.FloatField()
    proj_score1 = models.FloatField()
    proj_score2 = models.FloatField()
    score1 = models.FloatField(null=True, blank=True)
    score2 = models.FloatField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the match
        """

        return f"{self.team1} vs {self.team2} on {self.date}"

    class Meta:
        """
        Metadata options
        """

        db_table = "matches"
        verbose_name_plural = "Matches"
