import { useEffect, useState, useMemo, useCallback } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";
import L from "leaflet";
import "leaflet-routing-machine";
import "leaflet/dist/leaflet.css";
import Card from "./Card.jsx";
import { getTypeColor, getTypeIcon } from "./data.js";

/* ── Fix default marker icons ── */
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

/* ── Create a colored SVG marker for each type ── */
function createColoredIcon(color, emoji) {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36">
      <defs>
        <filter id="s" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000" flood-opacity="0.18"/>
        </filter>
      </defs>
      <g filter="url(#s)">
        <circle cx="18" cy="12" r="11" fill="#ffffff" stroke="${color}" stroke-width="3" />
        <circle cx="18" cy="12" r="6" fill="#ffffff" />
        <text x="18" y="15" text-anchor="middle" font-size="12">${emoji}</text>
      </g>
    </svg>`;

  return L.divIcon({
    html: svg,
    className: "custom-marker-icon",
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -26],
  });
}

/* ── Hotel marker ── */
const HOTEL_ICON = createColoredIcon("#f39c12", "🏨");

/* ── Route legs: one color per segment (library default was red-only) ── */
const SEGMENT_LINE_COLORS = [
  "#2563eb",
  "#059669",
  "#7c3aed",
  "#d97706",
  "#0891b2",
  "#4f46e5",
  "#0d9488",
  "#9333ea",
];

function lineStylesForSegment(segmentIndex) {
  const color = SEGMENT_LINE_COLORS[segmentIndex % SEGMENT_LINE_COLORS.length];
  return [
    { color: "#0f172a", opacity: 0.08, weight: 12 },
    { color: "#ffffff", opacity: 0.9, weight: 6 },
    { color, opacity: 0.98, weight: 4, dashArray: "8,8" },
  ];
}

/* One routing control per consecutive pair so each leg gets its own color */
const RoutingSegments = ({ waypoints }) => {
  const map = useMap();

  useEffect(() => {
    if (!map || !waypoints || waypoints.length < 2) return;

    const controls = [];
    for (let i = 0; i < waypoints.length - 1; i++) {
      const c = L.Routing.control({
        waypoints: [
          L.latLng(waypoints[i][0], waypoints[i][1]),
          L.latLng(waypoints[i + 1][0], waypoints[i + 1][1]),
        ],
        routeWhileDragging: false,
        createMarker: () => null,
        show: false,
        lineOptions: {
          styles: lineStylesForSegment(i),
          addWaypoints: false,
          extendToWaypoints: true,
        },
      }).addTo(map);
      controls.push(c);
    }

    return () => {
      controls.forEach((ctrl) => {
        try {
          if (ctrl && ctrl._map) {
            map.removeControl(ctrl);
          }
        } catch (error) {
          console.warn("Routing cleanup failed", error);
        }
      });
    };
  }, [map, waypoints]);

  return null;
};

/* ── Fly-to handler ── */
const FlyTo = ({ target }) => {
  const map = useMap();

  useEffect(() => {
    if (!target) return;
    map.flyTo([target.latitude, target.longitude], 15, { duration: 0.8 });
  }, [map, target]);

  return null;
};

/* ═══════════════════════════════════════════════════════
   MapComponent
   ═══════════════════════════════════════════════════════ */
const MapComponent = ({
  landmarks = [],
  hotels = [],
  startingHotel = 1,
  destinationHotel = 1,
  highlightId = null,
  showHotels = false,
  onMarkerClick,
  onToggleSidebar,
  style = {},
}) => {
  /* ── Icon cache ── */
  const iconCache = useMemo(() => {
    const cache = {};
    landmarks.forEach((lm) => {
      const key = lm.type;
      if (!cache[key]) {
        cache[key] = createColoredIcon(getTypeColor(key), getTypeIcon(key));
      }
    });
    return cache;
  }, [landmarks]);

  /* ── Highlighted landmark ── */
  const highlighted = useMemo(
    () => (highlightId != null ? landmarks.find((l) => l.id === highlightId) : null),
    [highlightId, landmarks]
  );

  /* ── Fallback centre (first landmark in visit order) ── */
  const center =
    landmarks.length > 0
      ? [landmarks[0].latitude, landmarks[0].longitude]
      : [36.7538, 3.0588];

const routeWaypoints = useMemo(() => {
  if (
    !hotels?.length ||
    hotels[startingHotel - 1] == null ||
    hotels[destinationHotel - 1] == null
  ) {
    return [];
  }

  return [
    // 1. Starting hotel
    [hotels[startingHotel - 1].latitude, hotels[startingHotel - 1].longitude],

    // 2. Spread the landmarks into the array
    ...landmarks.map((lm) => [lm.latitude, lm.longitude]),

    // 3. Destination hotel
    [hotels[destinationHotel - 1].latitude, hotels[destinationHotel - 1].longitude],
  ];
}, [landmarks, hotels, startingHotel, destinationHotel]);

  const startHotel = hotels[startingHotel - 1] || null;
  const destHotel = hotels[destinationHotel  - 1] || null;

  if (landmarks.length === 0 && hotels.length === 0) {
    return (
      <div className="map-empty">
        <span className="map-empty-icon">🗺️</span>
        <p>Loading map data…</p>
      </div>
    );
  }
  const Controls = () => {
    const map = useMap();
    return (
      <>
        <div className="map-controls">
          <button className="map-control-button" type="button" onClick={() => map.zoomIn()}>
            +
          </button>
          <button className="map-control-button" type="button" onClick={() => map.zoomOut()}>
            −
          </button>
          <button className="map-control-button" type="button" onClick={() => map.setView(center, 13)} aria-label="Center map">
            ⊙
          </button>
          <button className="map-control-button" type="button" onClick={onToggleSidebar} aria-label="Toggle sidebar">
            ☰
          </button>
        </div>
        <div className="map-badges">
          <div className="map-badge">Live Weather: 24°C • Sunny</div>
          <div className="map-badge">© 2024 Mediterranean AI</div>
        </div>
      </>
    );
  };

  return (
    <div style={{ position: "relative", height: "100%" }} className="map-wrapper">
      <MapContainer
        center={center}
        zoom={12}
        zoomControl={false}
        style={{ height: "100%", width: "100%", minHeight: "100vh", ...style }}
        className="main-map"
      >
        <Controls />
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
      />

      {/* ── Landmark markers ── */}
      {landmarks.map((lm) => (
        <Marker
          key={`landmark-${lm.id}`}
          position={[lm.latitude, lm.longitude]}
          icon={iconCache[lm.type] || iconCache[Object.keys(iconCache)[0]]}
          eventHandlers={{
            click: () => onMarkerClick?.(lm),
          }}
        >
          <Popup className="card-popup" maxWidth={260} minWidth={220}>
            <Card landmark={lm} compact />
          </Popup>
        </Marker>
      ))}

      {/* ── Hotel markers ── */}
      {showHotels &&
        hotels.map((h, i) => (
          <Marker
            key={`hotel-${i}`}
            position={[h.latitude, h.longitude]}
            icon={HOTEL_ICON}
          >
            <Popup>
              <div style={{ fontFamily: "'Inter', sans-serif", padding: 4 }}>
                <strong style={{ fontSize: 13 }}>🏨 {h.name}</strong>
              </div>
            </Popup>
          </Marker>
        ))}

      { startHotel && destHotel && (
        <>
          <Marker
            key={`hotel-start-${startingHotel}`}
            position={[startHotel.latitude, startHotel.longitude]}
            icon={HOTEL_ICON}
          >
            <Popup>
              <div style={{ fontFamily: "'Inter', sans-serif", padding: 4 }}>
                <strong style={{ fontSize: 13 }}>🏨 {startHotel.name}</strong>
              </div>
            </Popup>
          </Marker>
          <Marker
            key={`hotel-dest-${destinationHotel}`}
            position={[destHotel.latitude, destHotel.longitude]}
            icon={HOTEL_ICON}
          >
            <Popup>
              <div style={{ fontFamily: "'Inter', sans-serif", padding: 4 }}>
                <strong style={{ fontSize: 13 }}>🏨 {destHotel.name}</strong>
              </div>
            </Popup>
          </Marker>
        </>
      )}

      {/* ── Routing (order matches landmarks array) ── */}
      {/* Temporarily disabled due to leaflet-routing-machine cleanup issues */}
      {routeWaypoints.length > 1 && <RoutingSegments waypoints={routeWaypoints} />}

      {/* ── Fly to highlighted ── */}
      <FlyTo target={highlighted} />
    </MapContainer>
    </div>
  );
};

export default MapComponent;