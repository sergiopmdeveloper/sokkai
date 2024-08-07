from unittest.mock import Mock, patch

import pandas as pd
import pytest
from django.core.management.base import CommandError

from matches.management.commands.seed_matches import Command
from matches.models import Match


def test_seed_matches_call_methods(seed_matches_command: Command):
    """
    Tests the handle method of the seed_matches command
    and expects that all the methods are called
    """

    download_match_data_mock = Mock()
    extract_columns_mock = Mock()
    generate_match_instances_mock = Mock()
    save_match_instances_mock = Mock()

    seed_matches_command._download_match_data = download_match_data_mock
    seed_matches_command._extract_columns = extract_columns_mock
    seed_matches_command._generate_match_instances = generate_match_instances_mock
    seed_matches_command._save_match_instances = save_match_instances_mock
    seed_matches_command._match_instances = []

    seed_matches_command.handle()

    download_match_data_mock.assert_called_once()
    extract_columns_mock.assert_called_once()
    generate_match_instances_mock.assert_called_once()
    save_match_instances_mock.assert_called_once()


def test_seed_matches_download_match_data_error(seed_matches_command: Command):
    """
    Tests the _download_match_data method of the
    seed_matches command and expects that an error is raised
    """

    with patch("pandas.read_csv") as read_csv_mock:
        read_csv_mock.side_effect = Exception

        with pytest.raises(CommandError, match="Error downloading matches data"):
            seed_matches_command._download_match_data()


def test_seed_matches_download_match_data_success(
    seed_matches_command: Command, match_df: pd.DataFrame
):
    """
    Tests the _download_match_data method of the seed_matches
    command and expects that the match DataFrame is set
    """

    with patch("pandas.read_csv") as read_csv_mock:
        read_csv_mock.return_value = match_df

        seed_matches_command._download_match_data()

        assert seed_matches_command._match_df.equals(match_df)


def test_seed_matches_extract_columns(
    seed_matches_command: Command, match_df: pd.DataFrame
):
    """
    Tests the _extract_columns method of the seed_matches
    command and expects that the columns are extracted
    """

    seed_matches_command._match_df = match_df

    seed_matches_command._extract_columns()

    assert seed_matches_command._match_df.columns.to_list() == [
        "season",
        "date",
        "league",
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


def test_seed_matches_generate_match_instances(
    seed_matches_command: Command, match_df: pd.DataFrame
):
    """
    Tests the _generate_match_instances method of the seed_matches
    command and expects that the match instances are generated
    """

    seed_matches_command._match_df = match_df

    seed_matches_command._extract_columns()
    seed_matches_command._generate_match_instances()

    assert all(
        isinstance(match, Match) for match in seed_matches_command._match_instances
    )


@pytest.mark.django_db
def test_seed_matches_save_match_instances(
    seed_matches_command: Command, match_df: pd.DataFrame
):
    """
    Tests the _save_match_instances method of the seed_matches
    command and expects that the match instances are saved
    """

    seed_matches_command._match_df = match_df

    seed_matches_command._extract_columns()
    seed_matches_command._generate_match_instances()

    seed_matches_command._match_instances[0].save()
    seed_matches_command._save_match_instances()

    assert Match.objects.count() == len(seed_matches_command._match_instances)
