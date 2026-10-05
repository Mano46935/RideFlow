import { useState } from "react";
import { reportUnmetDemand } from "../api.js";

// Rider-side feature: "I looked for a driver here and couldn't find one".
// In the real app this would sit in the rider app behind login, and the
// user id would come from the session instead of a text box.
export default function UnmetDemandForm({ vehicle }) {
  const [userId, setUserId] = useState("");
  const [area, setArea] = useState("");
  const [message, setMessage] = useState("");
  const [failed, setFailed] = useState(false);

  async function handleSubmit() {
    setMessage("");
    try {
      await reportUnmetDemand({ userId, area, vehicleType: vehicle });
      setFailed(false);
      setMessage("Thanks, your report was saved.");
      setArea("");
    } catch (err) {
      setFailed(true);
      setMessage(err.message);
    }
  }

  return (
    <details className="card">
      <summary>Rider: report an unsuccessful search</summary>
      <p className="hint">You can send one report per day. It counts as demand, not as a booking.</p>
      <label>
        Rider ID
        <input value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="e.g. rider-101" />
      </label>
      <label>
        Area
        <input value={area} onChange={(e) => setArea(e.target.value)} placeholder="e.g. Anna Nagar" />
      </label>
      <button type="button" onClick={handleSubmit} disabled={!userId || !area}>
        Send report
      </button>
      {message && <p className={failed ? "error" : "success"}>{message}</p>}
    </details>
  );
}
