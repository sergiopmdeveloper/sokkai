from enum import Enum

MATCHES_DATA_URL = (
    "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv"
)


class MatchFields(Enum):
    DATE = "date"
    LEAGUE = "league"
    SEASON = "season"
    TEAM1 = "team1"
    TEAM2 = "team2"
    SPI1 = "spi1"
    SPI2 = "spi2"
    PROB1 = "prob1"
    PROB2 = "prob2"
    PROBTIE = "probtie"
    PROJSCORE1 = "proj_score1"
    PROJSCORE2 = "proj_score2"
    SCORE1 = "score1"
    SCORE2 = "score2"
