import { useState } from "react";
import { reportRideFound } from "../api.js";

function getDriverId() {
  const storageKey = "ride-demand-driver-id";
  let driverId = localStorage.getItem(storageKey);
  if (!driverId) {
    const id = globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    driverId = `captain-${id}`;
    localStorage.setItem(storageKey, driverId);
  }
  return driverId;
}

export default function RideFoundButton({ vehicleType }) {
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleRideFound() {
    setSaving(true);
    setMessage("");
    setError("");
    try {
      if (!navigator.geolocation) {
        throw new Error("This browser does not support location sharing.");
      }

      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 15000,
          maximumAge: 0,
        });
      });

      await reportRideFound({
        driverId: getDriverId(),
        vehicleType,
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
      });
      setMessage("Ride location recorded. Thanks!");
    } catch (err) {
      setError(err.message || "Could not record this ride. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="card">
      <h2>Found a ride?</h2>
      <p className="hint">Tap to share your current GPS location and help improve demand estimates.</p>
      <button
        type="button"
        className="ride-found"
        onClick={handleRideFound}
        disabled={saving}
      >
        {saving ? "Recording location..." : "I found a ride here"}
      </button>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </section>
  );
}
