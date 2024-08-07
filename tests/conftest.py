import pandas as pd
import pytest
from django.test import Client

from matches.management.commands.seed_matches import Command


@pytest.fixture
def client() -> Client:
    """
    Client fixture
    """

    return Client()


@pytest.fixture
def seed_matches_command() -> Command:
    """
    Seed matches command fixture
    """

    return Command()


@pytest.fixture
def match_df() -> pd.DataFrame:
    """
    Match DataFrame fixture
    """

    return pd.DataFrame(
        [
            {
                "season": 2017,
                "date": "2017-10-15",
                "league_id": 1854,
                "league": "Italy Serie A",
                "team1": "Internazionale",
                "team2": "AC Milan",
                "spi1": 78.3,
                "spi2": 71.94,
                "prob1": 0.5266,
                "prob2": 0.2279,
                "probtie": 0.2455,
                "proj_score1": 1.84,
                "proj_score2": 1.14,
                "importance1": 66.1,
                "importance2": 40.9,
                "score1": 3.0,
                "score2": 2.0,
                "xg1": 2.68,
                "xg2": 1.07,
                "nsxg1": 1.13,
                "nsxg2": 1.51,
                "adj_score1": 3.15,
                "adj_score2": 2.1,
            },
            {
                "season": 2017,
                "date": "2017-10-15",
                "league_id": 1869,
                "league": "Spanish Primera Division",
                "team1": "Real Betis",
                "team2": "Valencia",
                "spi1": 70.39,
                "spi2": 74.98,
                "prob1": 0.4274,
                "prob2": 0.3227,
                "probtie": 0.2499,
                "proj_score1": 1.59,
                "proj_score2": 1.35,
                "importance1": 41.0,
                "importance2": 60.6,
                "score1": 3.0,
                "score2": 6.0,
                "xg1": 2.42,
                "xg2": 1.83,
                "nsxg1": 2.04,
                "nsxg2": 1.44,
                "adj_score1": 3.15,
                "adj_score2": 5.22,
            },
            {
                "season": 2017,
                "date": "2017-10-15",
                "league_id": 1843,
                "league": "French Ligue 1",
                "team1": "Strasbourg",
                "team2": "Marseille",
                "spi1": 43.63,
                "spi2": 69.17,
                "prob1": 0.213,
                "prob2": 0.5493,
                "probtie": 0.2377,
                "proj_score1": 1.07,
                "proj_score2": 1.86,
                "importance1": 43.4,
                "importance2": 49.7,
                "score1": 3.0,
                "score2": 3.0,
                "xg1": 2.23,
                "xg2": 3.16,
                "nsxg1": 1.78,
                "nsxg2": 1.84,
                "adj_score1": 3.15,
                "adj_score2": 3.15,
            },
        ]
    )
