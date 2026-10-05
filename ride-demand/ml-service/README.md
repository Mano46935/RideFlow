# ML service (Python)

```bash
pip install -r requirements.txt

python generate_placeholder_data.py   # fake data -> data/rides.csv (skip if you have the real CSV)
python train.py                       # trains XGBoost, prints MAE / RMSE / F1 / ROC-AUC, saves models/demand_model.joblib
uvicorn predict_service:app --port 8000
```

The real CSV must have these columns: `Date`, `Time`, `Pickup Location`, `Vehicle Type`.
To retrain later with fresh data from PostgreSQL, export it to a CSV with the same columns and run `python train.py --data new_rides.csv`.
