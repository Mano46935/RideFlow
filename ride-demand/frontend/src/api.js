// all calls to the Spring Boot backend live here

async function post(url, body, extraHeaders = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...extraHeaders },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let message = "Something went wrong. Please try again.";
    try {
      const data = await res.json();
      if (data.message) message = data.message;
    } catch {
      // response had no json body, keep the default message
    }
    throw new Error(message);
  }
  return res.json();
}

export function predictDemand({ latitude, longitude, vehicle, time }) {
  return post("/api/demand/predict", { latitude, longitude, vehicle, time });
}

export function reportUnmetDemand({ userId, area, vehicleType }) {
  return post("/api/reports/unmet-demand", { area, vehicleType }, { "X-User-Id": userId });
}

export function reportRideFound({ driverId, vehicleType, latitude, longitude }) {
  return post("/api/observations/ride-found", {
    driverId,
    vehicleType,
    latitude,
    longitude,
    consent: true,
  });
}
