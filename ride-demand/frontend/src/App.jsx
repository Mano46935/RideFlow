import { useState } from "react";
import { predictDemand } from "./api.js";
import SearchPanel from "./components/SearchPanel.jsx";
import ResultsList from "./components/ResultsList.jsx";
import UnmetDemandForm from "./components/UnmetDemandForm.jsx";
import DemandMap from "./components/DemandMap.jsx";
import RideFoundButton from "./components/RideFoundButton.jsx";

export default function App() {
  // starting values: Gurugram, evening rush
  const [search, setSearch] = useState({
    latitude: 28.4593,
    longitude: 77.0727,
    vehicle: "Auto",
    time: "19:00",
  });
  const [areas, setAreas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  async function handlePredict() {
    setLoading(true);
    setError("");
    try {
      const data = await predictDemand(search);
      setAreas(data.areas);
      setSearched(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>Where should I go next?</h1>
        <p className="subtitle">Estimate customers by nearby pickup area, vehicle and time.</p>

        <SearchPanel search={search} onChange={setSearch} onPredict={handlePredict} loading={loading} />

        {error && <p className="error">{error}</p>}

        <ResultsList areas={areas} searched={searched} />

        <RideFoundButton vehicleType={search.vehicle} />

        <UnmetDemandForm vehicle={search.vehicle} />
      </aside>

      <main className="map-area">
        <DemandMap driver={search} areas={areas} />
      </main>
    </div>
  );
}
