

from typing import Any, Callable
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt

from cleaning import Cleaning


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

    def draw(self, predictions, y_actual):
        plt.figure(figsize=(8, 6))

        plt.scatter(
            predictions,
            y_actual,
            alpha=0.5,
            c="royalblue",
            edgecolors="k",
            label="Vins",
        )

        mn = min(predictions.min(), y_actual.min())
        mx = max(predictions.max(), y_actual.max())
        plt.plot(
            [mn, mx],
            [mn, mx],
            color="red",
            linestyle="--",
            lw=2,
            label="Prédiction Parfaite",
        )

        plt.xlabel("Prix estimés (estim_LR)")
        plt.ylabel("Prix réels (y_test)")
        plt.title("titre")
        plt.legend()
        plt.grid(True, linestyle=":", alpha=0.6)

        plt.show()


df_vins = (
    Cleaning("data.csv")
    .drop_empty_appellation()
    .fill_missing_scores()
    .encode_appellation()
    .drop_empty_price()
    .getVins()
)

etude = Learning(df_vins, target="Prix")

print("--- Question 16 & 17 ---")
score_simple, estim_simple = etude.evaluate(LinearRegression())
print(f"Score R² (LR Simple) : {score_simple:.4f}")

etude.draw(estim_simple, etude.y_test)


print("\n--- Question 18 ---")
score_std, estim_std = etude.evaluate(
    estimator=LinearRegression(), pretreatment=StandardScaler()
)
print(f"Score R² (Standardisation + LR) : {score_std:.4f}")

etude.draw(estim_std, etude.y_test)
