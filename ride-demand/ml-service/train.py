"""
Trains the demand models.

    python train.py                       # uses data/rides.csv
    python train.py --data my_export.csv  # e.g. rides exported from PostgreSQL

Steps: load -> clean -> count rides per area/vehicle/hour -> split by date
-> train XGBoost (regression + classification) -> evaluate -> save.
"""
import argparse
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, mean_absolute_error, mean_squared_error, roc_auc_score
from xgboost import XGBClassifier, XGBRegressor

from features import make_features


def load_rides(path):
    df = pd.read_csv(path)
    # build one datetime from the Date and Time columns
    df["datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce")
    # drop rows we can't use
    df = df.dropna(subset=["datetime", "Pickup Location", "Vehicle Type"])
    df["Pickup Location"] = df["Pickup Location"].str.strip()
    return df


def count_rides(df):
    """Raw bookings -> one row per (area, vehicle, date, hour) with a ride count."""
    df["date"] = df["datetime"].dt.normalize()
    df["hour"] = df["datetime"].dt.hour

    counts = (
        df.groupby(["Pickup Location", "Vehicle Type", "date", "hour"])
        .size()
        .reset_index(name="rides")
        .rename(columns={"Pickup Location": "area", "Vehicle Type": "vehicle"})
    )
    counts["day_of_week"] = counts["date"].dt.dayofweek  # Monday = 0
    counts["month"] = counts["date"].dt.month
    # note: hours with zero bookings have no row here. Fine for a first version.
    return counts


def main(data_path, model_path, head=None):
    rides = load_rides(data_path)
    if head is not None:
        rides = rides.head(head).copy()
        print(f"Training on first {len(rides)} rows from {data_path}")
    data = count_rides(rides)
    print(f"{len(rides)} rides -> {len(data)} area/hour rows")

    # test set = the latest 20% of dates, so we test on "the future"
    all_dates = np.sort(data["date"].unique())
    cutoff = all_dates[int(len(all_dates) * 0.8)]
    train = data[data["date"] < cutoff].copy()
    test = data[data["date"] >= cutoff].copy()

    # lookups the model needs later, learned from training data only
    art = {
        "area_codes": {a: i for i, a in enumerate(sorted(data["area"].unique()))},
        "vehicle_codes": {v: i for i, v in enumerate(sorted(data["vehicle"].unique()))},
        "past_demand": train.groupby(["area", "vehicle", "hour"])["rides"].mean().to_dict(),
        "global_mean": float(train["rides"].mean()),
        # "high demand" = busier than 75% of the training rows
        "high_demand_threshold": float(train["rides"].quantile(0.75)),
    }

    X_train, X_test = make_features(train, art), make_features(test, art)
    y_train, y_test = train["rides"], test["rides"]

    threshold = float(art["high_demand_threshold"])
    if y_train.nunique() > 1:
        # If the 10k sample is skewed, fallback to the median so at least two classes exist.
        if (y_train >= threshold).nunique() < 2:
            threshold = float(y_train.median())
            art["high_demand_threshold"] = threshold
    else:
        threshold = float(y_train.median())
        art["high_demand_threshold"] = threshold

    y_train_high = (y_train >= threshold).astype(int)
    y_test_high = (y_test >= threshold).astype(int)

    settings = dict(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    reg = XGBRegressor(**settings).fit(X_train, y_train)
    clf = None
    if y_train_high.nunique() > 1:
        clf = XGBClassifier(**settings).fit(X_train, y_train_high)

    # ---- evaluation ----
    pred = reg.predict(X_test)
    baseline = X_test["past_demand"]  # "just use the historical average"
    print("\nExpected rides")
    print(f"  MAE      model {mean_absolute_error(y_test, pred):.3f}   baseline {mean_absolute_error(y_test, baseline):.3f}")
    print(f"  RMSE     model {np.sqrt(mean_squared_error(y_test, pred)):.3f}   baseline {np.sqrt(mean_squared_error(y_test, baseline)):.3f}")

    if clf is not None:
        prob = clf.predict_proba(X_test)[:, 1]
        print("High-demand classifier")
        print(f"  F1       {f1_score(y_test_high, prob >= 0.5):.3f}")
        print(f"  ROC-AUC  {roc_auc_score(y_test_high, prob):.3f}")
    else:
        prob = np.full(len(X_test), 0.5)
        print("High-demand classifier")
        print("  F1       skipped (only one demand class in training data)")
        print("  ROC-AUC  skipped (only one demand class in training data)")

    art["reg"], art["clf"] = reg, clf
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(art, model_path)
    print(f"\nSaved model to {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/rides.csv")
    parser.add_argument("--model", default="models/demand_model.joblib")
    parser.add_argument("--head", type=int, default=None, help="Use only the first N rows for a quick training run.")
    args = parser.parse_args()
    main(args.data, args.model, args.head)
