import argparse
import os

import pandas as pd


def build_balanced_sample(data_path, output_path, target_rows=50000, random_state=42):
    df = pd.read_csv(data_path)
    required = {"Date", "Time", "Vehicle Type", "Pickup Location"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce")
    df = df.dropna(subset=["datetime", "Vehicle Type", "Pickup Location"]).copy()
    df["date"] = df["datetime"].dt.normalize()
    df["hour"] = df["datetime"].dt.hour

    area_hour_counts = (
        df.groupby(["Pickup Location", "Vehicle Type", "date", "hour"], as_index=False)
        .size()
        .rename(columns={"size": "rides"})
    )
    threshold = float(area_hour_counts["rides"].quantile(0.75))
    area_hour_counts["high_demand"] = area_hour_counts["rides"] >= threshold

    vehicles = sorted(df["Vehicle Type"].dropna().unique().tolist())
    if not vehicles:
        raise ValueError("No vehicle types found in the dataset.")

    rows_per_vehicle = target_rows // len(vehicles)
    rows_per_class = rows_per_vehicle // 2
    selected_frames = []

    for vehicle in vehicles:
        vehicle_groups = area_hour_counts[area_hour_counts["Vehicle Type"] == vehicle].copy()
        low_groups = vehicle_groups[~vehicle_groups["high_demand"]]
        high_groups = vehicle_groups[vehicle_groups["high_demand"]]

        low_groups = low_groups.sample(n=min(len(low_groups), rows_per_class), random_state=random_state)
        high_groups = high_groups.sample(n=min(len(high_groups), rows_per_class), random_state=random_state + 1)

        for _, group in low_groups.iterrows():
            subset = df[
                (df["Vehicle Type"] == vehicle)
                & (df["Pickup Location"] == group["Pickup Location"])
                & (df["date"] == group["date"])
                & (df["hour"] == group["hour"])
            ]
            if len(subset) > 0:
                selected_frames.append(subset.sample(n=min(len(subset), 1), random_state=random_state))

        for _, group in high_groups.iterrows():
            subset = df[
                (df["Vehicle Type"] == vehicle)
                & (df["Pickup Location"] == group["Pickup Location"])
                & (df["date"] == group["date"])
                & (df["hour"] == group["hour"])
            ]
            if len(subset) > 0:
                selected_frames.append(subset.sample(n=min(len(subset), 1), random_state=random_state + 2))

    sample = pd.concat(selected_frames, ignore_index=True) if selected_frames else df.head(0)
    if len(sample) > target_rows:
        sample = sample.sample(n=target_rows, random_state=random_state)

    if len(sample) < target_rows:
        extra = df[~df.index.isin(sample.index)].sample(n=target_rows - len(sample), random_state=random_state)
        sample = pd.concat([sample, extra], ignore_index=True)

    sample = sample.drop(columns=["datetime", "date", "hour"], errors="ignore")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sample.to_csv(output_path, index=False)
    print(f"Balanced sample written to {output_path}")
    print(f"Rows: {len(sample)}")
    print(sample["Vehicle Type"].value_counts().to_dict())
    print("High demand rows in sample:", int((sample["Vehicle Type"].notna()).sum()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/rides.csv")
    parser.add_argument("--output", default="data/ride_sample_balanced_50k.csv")
    parser.add_argument("--target", type=int, default=50000)
    args = parser.parse_args()
    build_balanced_sample(args.data, args.output, target_rows=args.target)
