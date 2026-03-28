#!/usr/bin/env python3

from typing import Any, Callable
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


class Learning:
    def __init__(self, vins: DataFrame, target: str) -> None:
        self.X = vins.drop(target, axis=1)
        self.y = vins[target]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.25, random_state=49
        )

    def evaluate(
        self,
        estimator,
        pretreatment=None,
        fn_score=lambda m, xt, yt: m.score(xt, yt),
    ):

        pipeline = make_pipeline(pretreatment, estimator) if pretreatment else estimator
        pipeline.fit(self.X_train, self.y_train)
        score = fn_score(pipeline, self.X_test, self.y_test)
        prediction = pipeline.predict(self.X_test)

        return score, prediction
