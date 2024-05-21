from unittest.mock import Mock

import numpy as np
import pandas as pd
import pytest

from matches.management.commands import train_match_winner_model
from matches.models import Match


@pytest.fixture
def command_instance() -> train_match_winner_model.Command:
    """
    Fixture to return an instance of the
    train_match_winner_model.Command class

    Returns
    -------
    train_match_winner_model.Command
        An instance of the train_match_winner_model.Command class
    """

    return train_match_winner_model.Command()


@pytest.fixture
def match_df_with_id(match_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fixture to return a match df
    with an id as the index

    Parameters
    ----------
    match_df : pd.DataFrame
        Match df fixture

    Returns
    -------
    pd.DataFrame
        A match df with an id as the index
    """

    match_df["id"] = range(1, len(match_df) + 1)
    match_df.set_index("id", inplace=True)

    return match_df


def test_get_match_df_queries_matches_table_and_sets_match_df_attribute(
    command_instance: train_match_winner_model.Command, match_df_with_id: pd.DataFrame
) -> None:
    """
    Test that the _get_match_df method queries the
    matches table and assigns it to the _match_df attribute

    Parameters
    ----------
    command_instance : train_match_winner_model.Command
        Command instance fixture
    match_df_with_id : pd.DataFrame
        Match df with id fixture
    """

    match_df_with_id_copy = match_df_with_id.copy()
    match_df_with_id_copy["id"] = match_df_with_id.index

    match_objects_mock = Mock()

    match_objects_mock.all.return_value.values.return_value = (
        match_df_with_id_copy.to_dict("records")
    )

    Match.objects = match_objects_mock

    command_instance._get_match_df()

    match_objects_mock.all.assert_called_once()
    pd.testing.assert_frame_equal(command_instance._match_df, match_df_with_id)


def test_split_xy_splits_match_df_into_expected_X_and_y(
    command_instance: train_match_winner_model.Command, match_df_with_id: pd.DataFrame
) -> None:
    """
    Test that the _split_xy method splits
    the match df into the expected X and y

    Parameters
    ----------
    command_instance : train_match_winner_model.Command
        Command instance fixture
    match_df_with_id : pd.DataFrame
        Match df with id fixture
    """

    command_instance._match_df = match_df_with_id

    command_instance._split_xy()

    expected_X = match_df_with_id[
        [
            "spi1",
            "spi2",
            "prob1",
            "prob2",
            "probtie",
            "proj_score1",
            "proj_score2",
        ]
    ]

    expected_y = match_df_with_id[["score1", "score2"]]

    pd.testing.assert_frame_equal(command_instance.X, expected_X)
    pd.testing.assert_frame_equal(command_instance.y, expected_y)
