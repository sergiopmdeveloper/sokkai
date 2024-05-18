from __future__ import annotations

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class SplitXY(BaseEstimator, TransformerMixin):
    """
    SplitXY custom transformer

    Attributes
    ----------
    feature_columns : list[str]
        List of feature columns
    target_columns : list[str]
        List of target columns

    Methods
    -------
    fit(X: pd.DataFrame, y: any = None) -> SplitXY
        Fit the transformer with no effect
    transform(X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]
        Split X and y
    """

    def __init__(self, feature_columns: list[str], target_columns: list[str]) -> None:
        """
        Initialize SplitXY transformer

        Parameters
        ----------
        feature_columns : list[str]
            List of feature columns
        target_columns : list[str]
            List of target columns
        """

        self.feature_columns = feature_columns
        self.target_columns = target_columns

    def fit(self, X: pd.DataFrame, y: any = None) -> SplitXY:
        """
        Fit the transformer with no effect

        Parameters
        ----------
        X : pd.DataFrame
            DataFrame with features and targets
        y : any, optional
            Not used, by default None

        Returns
        -------
        SplitXY
            The transformer
        """

        return self

    def transform(self, X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split X and y

        Parameters
        ----------
        X : pd.DataFrame
            DataFrame with features and targets

        Returns
        -------
        tuple[pd.DataFrame, pd.DataFrame]
            X and Y
        """

        y = X[self.target_columns]
        X = X[self.feature_columns]

        return X, y
