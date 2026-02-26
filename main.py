#!/usr/bin/env python3

from os import getcwd
from os.path import normpath, join
from sys import argv
from pandas import read_csv, DataFrame

from cleaning import (display_info,
                      drop_empty_appellation,
                      mean_robert,
                      mean_robinson,
                      mean_suckling)


def load_csv(filename: str) -> DataFrame:
    path: str = normpath(join(getcwd(), filename))
    return read_csv(path)


def save_csv(df: DataFrame, out_filename: str) -> None:
    df.to_csv(out_filename, index=False)


def main() -> None:
    if len(argv) != 2:
        raise ValueError(f"Usage: {argv[0]} <filename.csv>")

    df = load_csv(argv[1])

    print("=== Avant nettoyage ===")
    display_info(df)

    df = drop_empty_appellation(df)
    save_csv(df, "donnee_clean.csv")

    print("\n=== Après nettoyage d'appellations manquantes ===")
    display_info(df)
    
    #la moyenne des notes des vins pour chaque appellation
    robert_means = mean_robert(df)
    save_csv(robert_means, "mean_robert_by_appellation.csv")
    print("\n=== moyenne Robert par appellation ===")
    print(robert_means.head(10))

    robinson_means = mean_robinson(df)
    save_csv(robinson_means, "mean_robinson_by_appellation.csv")
    print("\n===: moyennes Robinson par appellation ===")
    print(robinson_means.head(10))
    
    suckling_means = mean_suckling(df)
    save_csv(suckling_means, "mean_suckling_by_appellation.csv")
    print("\n===: moyennes Suckling par appellation ===")
    print(suckling_means.head(10))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERREUR: {e}")