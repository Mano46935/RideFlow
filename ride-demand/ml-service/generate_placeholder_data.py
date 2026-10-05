"""
Makes a fake ride-booking CSV so the whole pipeline can run end to end.

When you have the real 150,000-row file, just drop it in as data/rides.csv.
Only these columns are needed: Date, Time, Pickup Location, Vehicle Type
(the rest are kept so the file looks like the real one).
"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# area -> how busy it usually is (made up)
AREAS = {
    "Anna Nagar": 1.6, "T. Nagar": 1.4, "Nungambakkam": 1.1, "Egmore": 0.8,
    "Adyar": 1.0, "Velachery": 1.2, "Guindy": 0.9, "Mylapore": 0.7,
}
VEHICLES = ["Bike", "Auto", "Mini", "Sedan"]
STATUSES = ["Completed", "Cancelled by Driver", "Cancelled by Customer", "No Driver Found"]
N_ROWS = 300_000


def hour_weight(h):
    # a small morning rush and a bigger evening rush
    return 0.2 + np.exp(-((h - 9) ** 2) / 8) + 1.3 * np.exp(-((h - 19) ** 2) / 6)


hours = np.arange(24)
hour_p = np.array([hour_weight(h) for h in hours])
hour_p = hour_p / hour_p.sum()

area_names = list(AREAS)
area_p = np.array(list(AREAS.values()))
area_p = area_p / area_p.sum()

# Fridays and weekends get a bit more traffic
all_days = pd.date_range("2024-01-01", "2024-12-31")
day_p = np.where(all_days.dayofweek >= 4, 1.3, 1.0)
day_p = day_p / day_p.sum()
dates = all_days[rng.choice(len(all_days), N_ROWS, p=day_p)]

hour = rng.choice(hours, N_ROWS, p=hour_p)
minute = rng.integers(0, 60, N_ROWS)

df = pd.DataFrame({
    "Date": dates.strftime("%Y-%m-%d"),
    "Time": [f"{h:02d}:{m:02d}:00" for h, m in zip(hour, minute)],
    "Booking Status": rng.choice(STATUSES, N_ROWS, p=[0.65, 0.15, 0.10, 0.10]),
    "Vehicle Type": rng.choice(VEHICLES, N_ROWS, p=[0.35, 0.30, 0.20, 0.15]),
    "Pickup Location": rng.choice(area_names, N_ROWS, p=area_p),
    "Booking Value": rng.integers(60, 600, N_ROWS),
    "Ride Distance": rng.uniform(1, 25, N_ROWS).round(1),
})

os.makedirs("data", exist_ok=True)
df.to_csv("data/rides.csv", index=False)
print(f"Saved {len(df)} placeholder rides to data/rides.csv")
