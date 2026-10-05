import { CircleMarker, MapContainer, Popup, TileLayer, useMap } from "react-leaflet";

// red = very busy, amber = medium, teal = quiet
export function demandColor(probability) {
  if (probability >= 0.7) return "#d6336c";
  if (probability >= 0.4) return "#f08c00";
  return "#1c7c8c";
}

// moves the map when the driver's location changes
function Recenter({ lat, lng }) {
  const map = useMap();
  map.setView([lat, lng]);
  return null;
}

export default function DemandMap({ driver, areas }) {
  return (
    <MapContainer center={[driver.latitude, driver.longitude]} zoom={13} className="map">
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      <Recenter lat={driver.latitude} lng={driver.longitude} />

      {/* the driver */}
      <CircleMarker
        center={[driver.latitude, driver.longitude]}
        radius={8}
        pathOptions={{ color: "#fff", weight: 3, fillColor: "#1864ab", fillOpacity: 1 }}
      >
        <Popup>You are here</Popup>
      </CircleMarker>

      {/* one bubble per area, bigger = more rides */}
      {areas.map((a) => (
        <CircleMarker
          key={a.area}
          center={[a.latitude, a.longitude]}
          radius={10 + a.expectedRides * 1.5}
          pathOptions={{
            color: demandColor(a.highDemandProbability),
            fillColor: demandColor(a.highDemandProbability),
            fillOpacity: 0.45,
            weight: 2,
          }}
        >
          <Popup>
            <strong>{a.area}</strong>
            <br />
            {a.expectedRides} rides &middot; {Math.round(a.highDemandProbability * 100)}% chance of high demand
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
