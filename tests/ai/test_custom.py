import pandas as pd
import pytest

from ai.custom import generate_match_winner_column


def test_generate_match_winner_column_returns_expected_values(
    match_df: pd.DataFrame,
) -> None:
    """
    Test if generate_match_winner_column returns expected values

    Parameters
    ----------
    match_df : pd.DataFrame
        Match df fixture
    """

    expected_match_winner_values = [0, 0, 1]

    result = generate_match_winner_column(df=match_df)

    assert result.tolist() == expected_match_winner_values
