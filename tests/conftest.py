import pandas as pd
import pytest


@pytest.fixture
def match_df() -> pd.DataFrame:
    """
    Fixture to return a DataFrame with match data

    Returns
    -------
    pd.DataFrame
        A DataFrame with match data
    """

    return pd.DataFrame(
        {
            "season": [2016, 2016, 2016],
            "date": ["2016-08-13", "2016-08-13", "2016-08-13"],
            "league_id": [1843, 1843, 1843],
            "league": ["French Ligue 1", "French Ligue 1", "French Ligue 1"],
            "team1": ["Metz", "Montpellier", "Dijon FCO"],
            "team2": ["Lille", "Angers", "Nantes"],
            "spi1": [54.34, 58.82, 55.0],
            "spi2": [66.1, 53.1, 54.9],
            "prob1": [0.3444, 0.4939, 0.4471],
            "prob2": [0.3479, 0.2109, 0.249],
            "probtie": [0.3077, 0.2952, 0.3038],
            "proj_score1": [1.18, 1.51, 1.4],
            "proj_score2": [1.3, 0.89, 1.01],
            "importance1": [26.9, 22.5, 29.2],
            "importance2": [48.7, 27.7, 25.6],
            "score1": [3.0, 1.0, 0.0],
            "score2": [2.0, 0.0, 1.0],
            "xg1": [2.35, 0.8, 0.3],
            "xg2": [1.87, 0.53, 1.17],
            "nsxg1": [0.68, 0.58, 0.81],
            "nsxg2": [1.26, 1.28, 0.87],
            "adj_score1": [3.15, 1.05, 0.0],
            "adj_score2": [2.1, 0.0, 1.05],
        }
    )
