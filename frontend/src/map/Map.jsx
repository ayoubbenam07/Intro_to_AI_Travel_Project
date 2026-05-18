import React, { useEffect, useState, useCallback, useMemo } from "react";
import MapComponent from "./MapComponent.jsx";
import { loadLandmarks, loadHotels, getTypeColor, getTypeIcon } from "./data.js";
import "./style.css";

/* ── Unique types for filter chips ── */
function getUniqueTypes(landmarks) {
  const set = new Set(landmarks.map((l) => l.type));
  return ["All", ...Array.from(set).sort()];
}

export default function Map() {
  const [landmarks, setLandmarks] = useState([]);
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showHotels, setShowHotels] = useState(false);
  const [highlightId, setHighlightId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  /** Landmark IDs in visit order — path and list follow this sequence (not sorted by id). */
  const targetIds = useMemo(() => [1, 39, 64, 4, 23, 3, 21, 28, 18, 11, 16, 13, 51, 24, 5, 2, 31, 62, 40, 38, 48, 57, 15, 44, 63, 58, 34, 42, 66, 45, 19, 14, 9, 59, 68], []);

  /* ── Load data ── */
  useEffect(() => {
    Promise.all([loadLandmarks(), loadHotels()])
      .then(([lm, ht]) => {
        setLandmarks(lm);
        setHotels(ht);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  /* ── Derived values ── */
  const types = useMemo(() => getUniqueTypes(landmarks), [landmarks]);

  const orderedLandmarks = useMemo(() => {
    if (!landmarks?.length) return [];
    return targetIds
      .map((id) => landmarks.find((l) => l.id === id))
      .filter(Boolean);
  }, [landmarks, targetIds]);

  /* ── Handlers ── */
  const handleCardClick = useCallback((lm) => {
    setHighlightId(lm.id);
  }, []);

  const handleMarkerClick = useCallback((lm) => {
    setHighlightId(lm.id);
    // scroll sidebar card into view
    const el = document.getElementById(`card-${lm.id}`);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
  }, []);

  const handleToggleSidebar = useCallback(() => {
    setSidebarOpen((open) => !open);
  }, []);

  if (loading) {
    return (
      <div className="loader-screen">
        <div className="loader-spinner" />
        <p>Loading Algiers landmarks…</p>
      </div>
    );
  }

  return (
    <div className="app-layout">
      {/* ═══ SIDEBAR ═══ */}
      <aside className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
        <div className={`sidebar-inner ${sidebarOpen ? "open" : "closed"}`}>
          {/* Hero section */}
          <div className="sidebar-hero">
            <span className="eyebrow">Explore Algiers</span>
            <h1>Let AI weave your perfect Mediterranean narrative.</h1>
            <p>
              Active intelligence routes for cultural discovery, coastal exploration, and
              unforgettable city moments.
            </p>
          </div>

          <div className="route-list">
            {orderedLandmarks.length === 0 && (
              <p className="no-results">No landmarks match your search.</p>
            )}
            {orderedLandmarks.map((lm, index) => (
              <article
                key={lm.id}
                id={`card-${lm.id}`}
                className={`route-card ${highlightId === lm.id ? "active" : ""}`}
                onClick={() => handleCardClick(lm)}
                role="button"
                tabIndex={0}
                onKeyDown={(event) => {
                  if (event.key === "Enter") handleCardClick(lm);
                }}
              >
                <div
                  className="route-card-icon"
                  style={{ background: `linear-gradient(135deg, ${getTypeColor(lm.type)}, ${getTypeColor(lm.type)}cc)` }}
                >
                  {getTypeIcon(lm.type)}
                </div>
                <div className="route-card-body">
                  <h2 className="route-card-title">{lm.name}</h2>
                  <div className="route-card-meta">
                    <span className="route-card-chip">{lm.type}</span>
                    <span>{lm.estimatedTime} min</span>
                    <span>{lm.rating.toFixed(1)} ★</span>
                  </div>
                </div>
              </article>
            ))}
          </div>

          <button
            className="generate-button"
            onClick={() => setShowHotels((v) => !v)}
            type="button"
          >
            {showHotels ? "Refresh AI Route" : "Generate AI Route"}
          </button>
        </div>
      </aside>

      {/* ═══ MAP ═══ */}
      <main className="map-area">
        <div className="map-ui-overlay">
          <div className="map-quickpanel">
            <p className="map-quickpanel-title">Live route briefing</p>
            <p className="map-quickpanel-text">
              Follow a curated itinerary through Algiers with coastal viewpoints, heritage
              stops, and local dining highlights.
            </p>
          </div>
        </div>
        

        <MapComponent
          landmarks={orderedLandmarks}
          hotels={hotels}
          highlightId={highlightId}
          startingHotel={1}
          destinationHotel={1}
          showHotels={showHotels}
          onMarkerClick={handleMarkerClick}
          onToggleSidebar={handleToggleSidebar}
        />
      </main>
    </div>
  );
}