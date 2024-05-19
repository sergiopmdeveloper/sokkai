from __future__ import annotations

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler


def split_xy(
    df: pd.DataFrame, feature_columns: list[str], target_columns: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split X and y from DataFrame

    Parameters
    ----------
    df : pd.DataFrame
        Match DataFrame with features and targets
    feature_columns : list[str]
        List with feature column names
    target_columns : list[str]
        List with target column names

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        Tuple with DataFrame with features and DataFrame with targets
    """

    X = df[feature_columns]
    y = df[target_columns]

    return X, y


class NumericalScaler(BaseEstimator, TransformerMixin):
    """
    NumericalScaler custom transformer

    Attributes
    ----------
    scaler : StandardScaler
        Scaler for numerical columns

    Methods
    -------
    fit(X: pd.DataFrame, _: pd.DataFrame) -> NumericalScaler
        Fit the scaler with the features
    transform(X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]
        Scale numerical columns and return
        both the DataFrame with scaled features
        and the DataFrame with targets
    """

    def __init__(self):
        """
        Initialize NumericalScaler
        """

        self.scaler = StandardScaler()

    def fit(self, X: pd.DataFrame, _: pd.DataFrame) -> NumericalScaler:
        """
        Fit the scaler with the features

        Parameters
        ----------
        X : pd.DataFrame
            DataFrame with features
        _ : pd.DataFrame
            DataFrame with targets

        Returns
        -------
        NumericalScaler
            The transformer
        """

        self.scaler.fit(X)

        return self

    def transform(self, X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Scale numerical columns and return
        both the DataFrame with scaled features
        and the DataFrame with targets

        Parameters
        ----------
        X : pd.DataFrame
            Match DataFrame with features

        Returns
        -------
        tuple[pd.DataFrame, pd.DataFrame]
            Tuple with DataFrame with scaled
            features and DataFrame with targets
        """

        X = X.copy()

        X[X.columns] = self.scaler.transform(X)

        return X
