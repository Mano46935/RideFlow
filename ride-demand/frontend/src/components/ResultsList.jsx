import { demandColor } from "./DemandMap.jsx";

export default function ResultsList({ areas, searched }) {
  if (!searched) return null;

  if (areas.length === 0) {
    return <p className="hint">No known pickup areas within range of this location.</p>;
  }

  return (
    <section className="card">
      <h2>Nearby demand</h2>
      <ol className="results">
        {areas.map((a) => (
          <li key={a.area}>
            <div className="result-top">
              <strong>{a.area}</strong>
              <span>{Math.round(a.highDemandProbability * 100)}%</span>
            </div>
            <div className="bar">
              <div
                className="bar-fill"
                style={{ width: `${a.highDemandProbability * 100}%`, background: demandColor(a.highDemandProbability) }}
              />
            </div>
            <div className="result-bottom">
              {a.expectedRides} rides expected &middot; {a.distanceKm} km away
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
