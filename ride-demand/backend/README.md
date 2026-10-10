# Backend (Spring Boot)

Needs Java 17, Maven and PostgreSQL.

1. Create a database: `createdb ride_demand` (edit `application.properties` if your credentials differ)
2. Start the Python ML service first (see `../ml-service/README.md`)
3. Run: `mvn spring-boot:run`  ->  http://localhost:8080

## Endpoints

| Method | Path | What it does |
|---|---|---|
| POST | `/api/demand/predict` | demand for areas near the driver, ranked |
| POST | `/api/demand/predict` | estimates distinct customers by nearby pickup area, vehicle and time |
| POST | `/api/reports/unmet-demand` | rider reports a failed search (header `X-User-Id`, once per day) |
| POST | `/api/observations` | driver app sends a location/online snapshot (needs `consent: true`) |
| POST | `/api/observations/ride-found` | captain records a found ride with GPS coordinates (needs `consent: true`) |

Example:

```bash
curl -X POST localhost:8080/api/demand/predict -H "Content-Type: application/json" \
  -d '{"latitude": 28.4593, "longitude": 77.0727, "vehicle": "Auto", "time": "19:00"}'
```

To record a ride found at the captain's current location:

```bash
curl -X POST localhost:8080/api/observations/ride-found -H "Content-Type: application/json" \
  -d '{"driverId": "captain-123", "vehicleType": "Auto", "latitude": 28.4593, "longitude": 77.0727, "consent": true}'
```
