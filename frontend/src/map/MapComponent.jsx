import { useEffect, useState, useMemo, useCallback } from "react";
import { FaMap, FaBed } from "react-icons/fa";
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
import { getTypeColor, getTypeIcon, getTypeIconSvg } from "./data.js";

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
function createColoredIcon(color, type) {
  const iconPath = getTypeIconSvg(type);
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="46" viewBox="0 0 40 46">
      <defs>
        <filter id="shadow-${type}" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#002366" flood-opacity="0.16"/>
        </filter>
      </defs>
      <g filter="url(#shadow-${type})">
        <!-- Tear drop map pin path -->
        <path d="M20 2C10.06 2 2 10.06 2 20c0 12.6 16.5 23.3 17.2 23.7a1.94 1.94 0 0 0 1.6 0c.7-.4 17.2-11.1 17.2-23.7 0-9.94-8.06-18-18-18z" fill="${color}" />
        <!-- Pristine core -->
        <circle cx="20" cy="18" r="10" fill="#ffffff" />
        <!-- Custom Vector Icon inside white core -->
        <g transform="translate(14, 12) scale(0.5)" stroke="${color}" fill="none">
          ${iconPath}
        </g>
      </g>
    </svg>`;

  return L.divIcon({
    html: svg,
    className: "custom-marker-icon",
    iconSize: [40, 46],
    iconAnchor: [20, 44],
    popupAnchor: [0, -42],
  });
}

/* ── Create a numbered SVG marker for itinerary order ── */
function createNumberedIcon(color, number) {
  const label = number > 99 ? "99+" : String(number);
  const fontSize = label.length > 1 ? "11" : "13";
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="52" viewBox="0 0 40 52">
      <defs>
        <filter id="shadow-num-${number}" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#002366" flood-opacity="0.22"/>
        </filter>
      </defs>
      <g filter="url(#shadow-num-${number})">
        <!-- Tear drop pin -->
        <path d="M20 2C10.06 2 2 10.06 2 20c0 12.6 16.5 23.3 17.2 23.7a1.94 1.94 0 0 0 1.6 0c.7-.4 17.2-11.1 17.2-23.7 0-9.94-8.06-18-18-18z" fill="${color}" />
        <!-- White circle core -->
        <circle cx="20" cy="19" r="11" fill="#ffffff" />
        <!-- Order number -->
        <text x="20" y="24" text-anchor="middle" font-size="${fontSize}" font-weight="bold" font-family="Inter, system-ui, sans-serif" fill="${color}">${label}</text>
      </g>
      <!-- Small order badge at top-right corner -->
      <circle cx="33" cy="7" r="7" fill="#0f172a" />
      <text x="33" y="11" text-anchor="middle" font-size="8" font-weight="bold" font-family="Inter, system-ui, sans-serif" fill="#ffffff">${label}</text>
    </svg>`;

  return L.divIcon({
    html: svg,
    className: "custom-marker-icon numbered-marker-icon",
    iconSize: [40, 52],
    iconAnchor: [20, 50],
    popupAnchor: [0, -48],
  });
}

/* ── Hotel marker ── */
const HOTEL_ICON = createColoredIcon("#f39c12", "Hotel");

/* ── Route legs: one color per segment (library default was red-only) ── */
const SEGMENT_LINE_COLORS = [
  "#0077be", // Primary Blue
  "#002366", // Tertiary Navy
  "#009688", // Ocean Teal
  "#3f51b5", // Mediterranean Indigo
  "#006aab", // Darker primary
  "#20b2aa", // Light ocean teal
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

    // Make a single routing request for all waypoints to prevent OSRM rate-limiting
    const control = L.Routing.control({
      waypoints: waypoints.map(wp => L.latLng(wp[0], wp[1])),
      routeWhileDragging: false,
      createMarker: () => null,
      show: false,
      lineOptions: {
        styles: [
          { color: "#0f172a", opacity: 0.15, weight: 10 },
          { color: "#ffffff", opacity: 0.9, weight: 6 },
          { color: "#0077be", opacity: 1, weight: 4, dashArray: "10,10" }
        ],
        addWaypoints: false,
        extendToWaypoints: true,
      },
    }).addTo(map);

    return () => {
      try {
        if (control && control._map) {
          map.removeControl(control);
        }
      } catch (error) {
        console.warn("Routing cleanup failed", error);
      }
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
  /* ── Icon cache (type-based, for non-itinerary use) ── */
  const iconCache = useMemo(() => {
    const cache = {};
    landmarks.forEach((lm) => {
      const key = lm.type;
      if (!cache[key]) {
        cache[key] = createColoredIcon(getTypeColor(key), key);
      }
    });
    return cache;
  }, [landmarks]);

  /* ── Numbered icon cache (one per landmark position in itinerary) ── */
  const numberedIconCache = useMemo(() => {
    return landmarks.map((lm, index) =>
      createNumberedIcon(getTypeColor(lm.type), index + 1)
    );
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
        <span className="map-empty-icon" style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
          <FaMap size={48} style={{ color: "var(--color-primary)", opacity: 0.8 }} />
        </span>
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
          {/* <button className="map-control-button" type="button" onClick={onToggleSidebar} aria-label="Toggle sidebar">
            ☰
          </button> */}
        </div>
        <div className="map-badges">
          <div className="map-badge">Live Weather: 24°C • Sunny</div>
          <div className="map-badge">© 2026 Algiers AI</div>
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
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
      />

      {/* ── Landmark markers (numbered in itinerary order) ── */}
      {landmarks.map((lm, index) => (
        <Marker
          key={`landmark-${lm.id}`}
          position={[lm.latitude, lm.longitude]}
          icon={numberedIconCache[index]}
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
              <div style={{ fontFamily: "var(--font-body)", padding: 4 }}>
                <strong style={{ fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
                  <FaBed style={{ color: "#f39c12" }} /> {h.name}
                </strong>
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
              <div style={{ fontFamily: "var(--font-body)", padding: 4 }}>
                <strong style={{ fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
                  <FaBed style={{ color: "#f39c12" }} /> {startHotel.name}
                </strong>
              </div>
            </Popup>
          </Marker>
          <Marker
            key={`hotel-dest-${destinationHotel}`}
            position={[destHotel.latitude, destHotel.longitude]}
            icon={HOTEL_ICON}
          >
            <Popup>
              <div style={{ fontFamily: "var(--font-body)", padding: 4 }}>
                <strong style={{ fontSize: 13, display: "flex", alignItems: "center", gap: 6 }}>
                  <FaBed style={{ color: "#f39c12" }} /> {destHotel.name}
                </strong>
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