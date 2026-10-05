import { useState } from "react";
import { predictDemand } from "./api.js";
import SearchPanel from "./components/SearchPanel.jsx";
import ResultsList from "./components/ResultsList.jsx";
import UnmetDemandForm from "./components/UnmetDemandForm.jsx";
import DemandMap from "./components/DemandMap.jsx";

export default function App() {
  // starting values: central Chennai, evening rush
  const [search, setSearch] = useState({
    latitude: 13.08,
    longitude: 80.27,
    vehicle: "Bike",
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
        <p className="subtitle">Pick your location and time to compare demand in nearby areas.</p>

        <SearchPanel search={search} onChange={setSearch} onPredict={handlePredict} loading={loading} />

        {error && <p className="error">{error}</p>}

        <ResultsList areas={areas} searched={searched} />

        <UnmetDemandForm vehicle={search.vehicle} />
      </aside>

      <main className="map-area">
        <DemandMap driver={search} areas={areas} />
      </main>
    </div>
  );
}
