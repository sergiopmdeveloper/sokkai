import numpy as np
import pandas as pd

from matches.constants import MatchFields

MATCH_WINNER_COLUMN = "winner"


def generate_match_winner_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate match winner column

    Parameters
    ----------
    df : pd.DataFrame
        Match DataFrame

    Returns
    -------
    pd.DataFrame
        Match DataFrame with match winner column
    """

    df = df.copy()

    match_winner_values = np.where(
        df[MatchFields.score1.value] > df[MatchFields.score2.value], 0, 1
    )

    df = pd.DataFrame(match_winner_values, columns=[MATCH_WINNER_COLUMN])

    return df
