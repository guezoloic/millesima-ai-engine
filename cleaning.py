#!/usr/bin/env python3
from pandas import DataFrame, to_numeric


def display_info(df: DataFrame) -> None:
    print(df.all())
    print(df.info())
    print("\nNombre de valeurs manquantes par colonne :")
    print(df.isna().sum())


def drop_empty_appellation(df: DataFrame) -> DataFrame:

    return df.dropna(subset=["Appellation"])


def mean_score(df: DataFrame, col: str) -> DataFrame:
    """
    Calcule la moyenne d'une colonne de score par appellation.
        - Convertit les valeurs en numériques, en remplaçant les non-convertibles par NaN
        - Calcule la moyenne par appellation
        - Remplace les NaN résultants par 0 

    """
    tmp = df[["Appellation", col]].copy()

    tmp[col] = to_numeric(tmp[col], errors="coerce")

    # moyenne par appellation
    means = tmp.groupby("Appellation", as_index=False)[col].mean()
    
    means[col] = means[col].fillna(0)
    
    means = means.rename(columns={col: f"mean_{col}"})
    
    return means


def mean_robert(df: DataFrame) -> DataFrame:
    return mean_score(df, "Robert")


def mean_robinson(df: DataFrame) -> DataFrame:
    return mean_score(df, "Robinson")


def mean_suckling(df: DataFrame) -> DataFrame:
    return mean_score(df, "Suckling")