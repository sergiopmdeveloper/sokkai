from enum import Enum

MATCH_DATA_URL = "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv"


class MatchFields(Enum):
    date = "date"
    league = "league"
    season = "season"
    team1 = "team1"
    team2 = "team2"
    spi1 = "spi1"
    spi2 = "spi2"
    prob1 = "prob1"
    prob2 = "prob2"
    probtie = "probtie"
    proj_score1 = "proj_score1"
    proj_score2 = "proj_score2"
    score1 = "score1"
    score2 = "score2"


class MatchFieldTypes(Enum):
    date = "datetime64[ns]"
    league = "object"
    season = "int64"
    team1 = "object"
    team2 = "object"
    spi1 = "float64"
    spi2 = "float64"
    prob1 = "float64"
    prob2 = "float64"
    probtie = "float64"
    proj_score1 = "float64"
    proj_score2 = "float64"
    score1 = "int64"
    score2 = "int64"


ALL_LEAGUES = "All leagues"
