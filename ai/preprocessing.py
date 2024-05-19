import pandas as pd


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
