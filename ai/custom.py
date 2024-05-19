from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from matches.constants import MatchFields


class GenerateMatchWinnerColumn(BaseEstimator, TransformerMixin):
    """
    GenerateMatchWinnerColumn custom transformer

    Attributes
    ----------
    MATCH_WINNER_COLUMN : str
        Column name for match winner

    Methods
    -------
    fit(_: pd.DataFrame, y: pd.DataFrame) -> GenerateMatchWinnerColumn
        Fit the transformer defining as attribute
        the DataFrame with match scores
    transform(X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]
        Generate match winner column and return both
        the match DataFrame with features and the
        match DataFrame with match winner column
    """

    MATCH_WINNER_COLUMN = "winner"

    def fit(self, _: pd.DataFrame, y: pd.DataFrame) -> GenerateMatchWinnerColumn:
        """
        Fit the transformer defining as attribute
        the DataFrame with match scores

        Parameters
        ----------
        _ : pd.DataFrame
            Match DataFrame with features
        y : pd.DataFrame
            Match DataFrame with targets

        Returns
        -------
        GenerateMatchWinnerColumn
            The transformer
        """

        self.y = y

        return self

    def transform(self, X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Generate match winner column and return both
        the match DataFrame with features and the
        match DataFrame with match winner column

        Parameters
        ----------
        X : pd.DataFrame
            Match DataFrame with features

        Returns
        -------
        tuple[pd.DataFrame, pd.DataFrame]
            Tuple with match DataFrame with features
            and match DataFrame with match winner column
        """

        match_winner_values = np.where(
            self.y[MatchFields.score1.value] > self.y[MatchFields.score2.value],
            0,
            1,
        )

        y = pd.DataFrame(data=match_winner_values, columns=[self.MATCH_WINNER_COLUMN])

        return X, y
