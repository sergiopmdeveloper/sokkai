from unittest.mock import patch
from urllib.error import HTTPError

import pandas as pd
import pytest

from matches.constants import MatchFields, MatchFieldsTypes
from matches.exceptions import DownloadError, FieldsNotFound
from matches.management.commands import populate_finished_matches
from matches.models import Match


@pytest.fixture
def command_instance() -> populate_finished_matches.Command:
    """
    Fixture to return an instance of the
    populate_finished_matches.Command class

    Returns
    -------
    populate_finished_matches.Command
        An instance of the populate_finished_matches.Command class
    """

    return populate_finished_matches.Command()


@pytest.fixture
def matches_df() -> pd.DataFrame:
    """
    Fixture to return a DataFrame with matches data

    Returns
    -------
    pd.DataFrame
        A DataFrame with matches data
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


def test_match_fields_and_match_fields_types_are_equal() -> None:
    """
    Test that the MatchFields and
    MatchFieldsTypes enums have the same fields
    """

    assert set(MatchFields.__members__.keys()) == set(
        MatchFieldsTypes.__members__.keys()
    )


def test_download_matches_data_read_csv_matches_data_url(
    command_instance: populate_finished_matches.Command,
) -> None:
    """
    Test that the _download_matches_data method calls
    the pd.read_csv function with the MATCHES_DATA_URL

    Parameters
    ----------
    command_instance : populate_finished_matches.Command
        Command instance fixture
    """

    with patch("pandas.read_csv") as mock_read_csv:
        command_instance._download_matches_data()

        mock_read_csv.assert_called_with(
            "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv"
        )


def test_download_matches_data_raises_download_error(
    command_instance: populate_finished_matches.Command,
) -> None:
    """
    Test that the _download_matches_data method raises
    a DownloadError if an HTTPError is raised

    Parameters
    ----------
    command_instance : populate_finished_matches.Command
        Command instance fixture
    """

    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.side_effect = HTTPError("", "", "", "", "")

        with pytest.raises(DownloadError) as exc_info:
            command_instance._download_matches_data()

        assert str(exc_info.value) == "Error downloading matches data"


def test_extract_matches_columns_selects_correct_columns(
    command_instance: populate_finished_matches.Command,
    matches_df: pd.DataFrame,
) -> None:
    """
    Test that the _extract_matches_columns method selects
    the correct columns from the matches data

    Parameters
    ----------
    command_instance : populate_finished_matches.Command
        Command instance fixture
    matches_df : pd.DataFrame
        Matches df fixture
    """

    command_instance.matches_df = matches_df

    command_instance._extract_matches_columns()

    assert list(command_instance.matches_df.columns) == [
        "date",
        "league",
        "season",
        "team1",
        "team2",
        "spi1",
        "spi2",
        "prob1",
        "prob2",
        "probtie",
        "proj_score1",
        "proj_score2",
        "score1",
        "score2",
    ]


def test_extract_matches_columns_raises_fields_not_found(
    command_instance: populate_finished_matches.Command,
    matches_df: pd.DataFrame,
) -> None:
    """
    Test that the _extract_matches_columns method raises
    a FieldsNotFound exception if a KeyError is raised

    Parameters
    ----------
    command_instance : populate_finished_matches.Command
        Command instance fixture
    matches_df : pd.DataFrame
        Matches df fixture
    """

    matches_df = matches_df.drop(
        columns=["date", "league", "season", "team1", "team2", "spi1", "spi2"]
    )

    command_instance.matches_df = matches_df

    with pytest.raises(FieldsNotFound) as exc_info:
        command_instance._extract_matches_columns()

    assert (
        str(exc_info.value)
        == "Fields ['date', 'league', 'season', 'team1', 'team2', 'spi1', 'spi2'] not found in matches data"
    )


def test_filter_finished_matches_selects_matches_with_scores(
    command_instance: populate_finished_matches.Command,
    matches_df: pd.DataFrame,
) -> None:
    """
    Test that the _filter_finished_matches method filters
    the matches data to only include matches with scores

    Parameters
    ----------
    command_instance : populate_finished_matches.Command,
        Command instance fixture
    matches_df : pd.DataFrame
        Matches df fixture
    """

    matches_df.loc[0, "score1"] = None
    matches_df.loc[1, "score2"] = None

    command_instance.matches_df = matches_df
    command_instance._filter_finished_matches()

    assert command_instance.matches_df.shape[0] == 1


def test_drop_nan_values_drops_nan_values(
    command_instance: populate_finished_matches.Command,
    matches_df: pd.DataFrame,
) -> None:
    """
    Test that the _drop_nan_values method drops NaN values
    from the matches data

    Parameters
    ----------
    command_instance : populate_finished_matches.Command
        Command instance fixture
    matches_df : pd.DataFrame
        Matches df fixture
    """

    matches_df.loc[0, "team1"] = None
    matches_df.loc[1, "spi2"] = None

    command_instance.matches_df = matches_df
    command_instance._drop_nan_values()

    assert command_instance.matches_df.shape[0] == 1


def test_reset_matches_table_sequence_resets_sequence(
    command_instance: populate_finished_matches.Command,
) -> None:
    """
    Test that the _reset_matches_table_sequence
    method resets the sequence of the matches table

    Parameters
    ----------
    command_instance : populate_finished_matches.Command,
        Command instance fixture
    """

    with patch("django.db.connection.cursor") as mock_cursor:
        command_instance._reset_matches_table_sequence()

        mock_cursor.return_value.__enter__.return_value.execute.assert_called_once_with(
            "DELETE FROM sqlite_sequence WHERE name='matches';"
        )


def test_set_matches_df_column_types_sets_column_types(
    command_instance: populate_finished_matches.Command,
    matches_df: pd.DataFrame,
) -> None:
    """
    Test that the _set_matches_df_column_types method sets
    the column types of the matches data

    Parameters
    ----------
    command_instance : populate_finished_matches.Command
        Command instance fixture
    matches_df : pd.DataFrame
        Matches df fixture
    """

    expected_match_fields_types = {
        "date": "datetime64[ns]",
        "league": "object",
        "season": "int64",
        "team1": "object",
        "team2": "object",
        "spi1": "float64",
        "spi2": "float64",
        "prob1": "float64",
        "prob2": "float64",
        "probtie": "float64",
        "proj_score1": "float64",
        "proj_score2": "float64",
        "score1": "int64",
        "score2": "int64",
    }

    command_instance.matches_df = matches_df
    command_instance._extract_matches_columns()
    command_instance._set_matches_df_column_types()

    for field, dtype in expected_match_fields_types.items():
        assert command_instance.matches_df[field].dtype == dtype


def test_insert_matches_in_db_calls_submethods(
    command_instance: populate_finished_matches.Command,
    matches_df: pd.DataFrame,
) -> None:
    """
    Test that the _insert_matches_in_db
    method calls the necessary submethods

    Parameters
    ----------
    command_instance : populate_finished_matches.Command
        Command instance fixture
    matches_df : pd.DataFrame
        Matches df fixture
    """

    command_instance.matches_df = matches_df
    command_instance._extract_matches_columns()
    command_instance._filter_finished_matches()
    command_instance._drop_nan_values()

    with (
        patch(
            "matches.management.commands.populate_finished_matches.Match.objects"
        ) as mock_match_objects,
        patch(
            "matches.management.commands.populate_finished_matches.Command._reset_matches_table_sequence"
        ) as mock_reset_sequence,
        patch(
            "matches.management.commands.populate_finished_matches.Command._set_matches_df_column_types"
        ) as mock_set_column_types,
    ):
        command_instance._insert_matches_in_db()

        mock_match_objects.all.return_value.delete.assert_called_once()
        mock_reset_sequence.assert_called_once()
        mock_set_column_types.assert_called_once()
        mock_match_objects.bulk_create.assert_called_once()
