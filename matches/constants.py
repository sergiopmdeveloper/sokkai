class MatchFields:
    """
    Match fields constants
    """

    SEASON = "season"
    DATE = "date"
    LEAGUE = "league"
    TEAM1 = "team1"
    TEAM2 = "team2"
    SPI1 = "spi1"
    SPI2 = "spi2"
    PROB1 = "prob1"
    PROB2 = "prob2"
    PROBTIE = "probtie"
    PROJ_SCORE1 = "proj_score1"
    PROJ_SCORE2 = "proj_score2"
    SCORE1 = "score1"
    SCORE2 = "score2"

    @classmethod
    def field_list(cls) -> list[str]:
        """
        Returns a list of all the fields
        """

        return [
            cls.SEASON,
            cls.DATE,
            cls.LEAGUE,
            cls.TEAM1,
            cls.TEAM2,
            cls.SPI1,
            cls.SPI2,
            cls.PROB1,
            cls.PROB2,
            cls.PROBTIE,
            cls.PROJ_SCORE1,
            cls.PROJ_SCORE2,
            cls.SCORE1,
            cls.SCORE2,
        ]
