"""Honest, time-ordered historical hindcasts for monsoon JJAS rainfall.

Forecast issue assumption: end of May of target year. Features include Jan–May
of target year and JJAS rainfall from preceding three years. No target-year
June–September rainfall is given to the models.

Fixed configuration; models are NOT selected or tuned using the 1996–2016 holdout.
Historical long-range hindcasts are not operational forecasts.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, balanced_accuracy_score,
    f1_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from .data import REGIONS, annual_with_anomaly, risk_label

TRAIN_END = 1995
HOLDOUT_START, HOLDOUT_END = 1996, 2016
FEATURES = ["JAN", "FEB", "MAR", "APR", "MAY", "jj_lag1", "jj_lag2", "jj_lag3"]
MODELS = ["Climatology", "Persistence", "Ridge ML", "Random Forest ML"]


def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = annual_with_anomaly(df).sort_values(["region", "year"]).copy()
    for lag in (1, 2, 3):
        df[f"jj_lag{lag}"] = df.groupby("region")["JJAS"].shift(lag)
    return df.dropna(subset=FEATURES + ["JJAS"])


def _models():
    return {
        "Ridge ML": make_pipeline(StandardScaler(), Ridge(alpha=10.0)),
        "Random Forest ML": RandomForestRegressor(
            n_estimators=180, max_depth=4, min_samples_leaf=6,
            random_state=42, n_jobs=1,
        ),
    }


def _score_region(data: pd.DataFrame, region: str):
    all_r = data[data.region == region].sort_values("year")
    train = all_r[all_r.year <= TRAIN_END].copy()
    test = all_r[(all_r.year >= HOLDOUT_START) & (all_r.year <= HOLDOUT_END)].copy()
    normal = float(train["reference_mm"].iloc[0])  # shared 1871–1995 reference; no test leakage
    y_actual = test["JJAS"].to_numpy(dtype=float)
    outputs = []
    predictions = {
        "Climatology": np.full(len(test), normal),
        "Persistence": test["jj_lag1"].to_numpy(dtype=float),
    }
    trained = {}
    for name, estimator in _models().items():
        estimator.fit(train[FEATURES], train["JJAS"])
        trained[name] = estimator
        predictions[name] = estimator.predict(test[FEATURES])
    for name, pred in predictions.items():
        actual_labels = [risk_label((a / normal - 1) * 100) for a in y_actual]
        predicted_labels = [risk_label((a / normal - 1) * 100) for a in pred]
        for year, observed, predicted, a_class, p_class in zip(
            test.year, y_actual, pred, actual_labels, predicted_labels
        ):
            outputs.append({
                "region": region, "year": int(year), "model": name,
                "observed_mm": round(float(observed), 4),
                "predicted_mm": round(float(predicted), 4),
                "observed_anomaly_pct": round((observed / normal - 1) * 100, 4),
                "predicted_anomaly_pct": round((predicted / normal - 1) * 100, 4),
                "actual_class": a_class, "predicted_class": p_class,
                "reference_mm": normal,
            })
    return outputs, trained


def build_results(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    features_df = make_features(data)
    all_outputs = []
    trained = {}
    for region in REGIONS:
        out, estimators = _score_region(features_df, region)
        all_outputs.extend(out)
        trained[region] = estimators
    pred_df = pd.DataFrame(all_outputs)
    scores = []
    for (region, model), group in pred_df.groupby(["region", "model"], sort=False):
        y_true = group["observed_mm"]
        y_pred = group["predicted_mm"]
        actual = group["actual_class"]
        forecasted = group["predicted_class"]
        scores.append({
            "region": region,
            "model": model,
            "n_test_years": int(len(group)),
            "mae_mm": round(float(mean_absolute_error(y_true, y_pred)), 3),
            "rmse_mm": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 3),
            "balanced_accuracy": round(float(balanced_accuracy_score(actual, forecasted)), 4),
            "macro_f1": round(float(f1_score(actual, forecasted, average="macro", zero_division=0)), 4),
        })
    return pred_df, pd.DataFrame(scores), trained


def validation_error_band(df: pd.DataFrame, region: str, model_name: str = "Ridge ML") -> float:
    """Approximate 80% absolute-error span from PRE-HOLDOUT 1981–1995 validation.
    This is *not* a calibrated prediction interval and should not be presented as one.
    """
    feat = make_features(df)
    d = feat[feat.region == region]
    train = d[(d.year >= 1874) & (d.year <= 1980)]
    val = d[(d.year >= 1981) & (d.year <= 1995)]
    if model_name not in _models():
        raise ValueError("Band only supported for ML models")
    model = _models()[model_name]
    model.fit(train[FEATURES], train["JJAS"])
    error = np.abs(val["JJAS"].to_numpy() - model.predict(val[FEATURES]))
    return float(np.quantile(error, 0.8))


if __name__ == "__main__":
    from .data import load_rainfall
    _, summary, _ = build_results(load_rainfall())
    print(summary.to_string(index=False))
