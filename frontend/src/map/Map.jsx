import React, { useEffect, useState, useCallback, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MapComponent from "./MapComponent.jsx";
import { loadLandmarks, loadHotels, getTypeColor, getTypeIcon } from "./data.js";
import "./style.css";

/* ── Unique types for filter chips ── */
function getUniqueTypes(landmarks) {
  const set = new Set(landmarks.map((l) => l.type));
  return ["All", ...Array.from(set).sort()];
}

export default function Map() {
  const location = useLocation();
  const navigate = useNavigate();
  const customItinerary = location.state?.itinerary;

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

  const customLandmarks = useMemo(() => {
    if (!customItinerary?.path) return null;
    return customItinerary.path.map((lm) => ({
      id: parseInt(lm.id, 10) || lm.id,
      name: lm.name,
      description: lm.description || "",
      type: lm.type,
      rating: lm.interest_score,
      latitude: lm.lat,
      longitude: lm.lon,
      estimatedTime: lm.visit_duration,
      icon: getTypeIcon(lm.type),
      color: getTypeColor(lm.type),
      arrivalInfo: customItinerary.time_plan?.[lm.name]
    }));
  }, [customItinerary]);

  const displayLandmarks = useMemo(() => {
    if (customLandmarks) return customLandmarks;
    
    if (!landmarks?.length) return [];
    return targetIds
      .map((id) => landmarks.find((l) => l.id === id))
      .filter(Boolean);
  }, [customLandmarks, landmarks, targetIds]);

  const startHotelIndex = useMemo(() => {
    if (!customItinerary || !hotels.length) return 1;
    const index = hotels.findIndex((h) => h.name === customItinerary.hotel);
    return index !== -1 ? index + 1 : 1;
  }, [customItinerary, hotels]);

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
          {customItinerary ? (
            <div className="sidebar-hero custom-hero" style={{ paddingBottom: '16px' }}>
              <span className="eyebrow">Optimized Itinerary</span>
              <h1 style={{ fontSize: '24px', lineHeight: '1.2', margin: '4px 0 12px' }}>Your Travel Plan is Ready</h1>
              <div className="ai-briefing-grid" style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: '12px',
                padding: '14px',
                borderRadius: '12px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                fontSize: '12px',
                color: 'var(--color-neutral-200)'
              }}>
                <div>
                  <span style={{ color: 'var(--color-neutral-400)', display: 'block', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Algorithm</span>
                  <strong>{customItinerary.algorithm}</strong>
                </div>
                <div>
                  <span style={{ color: 'var(--color-neutral-400)', display: 'block', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Runtime</span>
                  <strong>{customItinerary.runtime_seconds}s</strong>
                </div>
                <div>
                  <span style={{ color: 'var(--color-neutral-400)', display: 'block', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Unified Score</span>
                  <strong>{customItinerary.evaluation_score}</strong>
                </div>
                <div>
                  <span style={{ color: 'var(--color-neutral-400)', display: 'block', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Hotel Base</span>
                  <strong style={{ display: 'block', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }} title={customItinerary.hotel}>{customItinerary.hotel}</strong>
                </div>
              </div>
            </div>
          ) : (
            <div className="sidebar-hero">
              <span className="eyebrow">Explore Algiers</span>
              <h1>Let us design your perfect Mediterranean narrative.</h1>
              <p>
                Optimized routes for cultural discovery, coastal exploration, and
                unforgettable city moments.
              </p>
            </div>
          )}

          <div className="route-list">
            {displayLandmarks.length === 0 && (
              <p className="no-results">No landmarks match your search.</p>
            )}
            {displayLandmarks.map((lm, index) => (
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
                    {lm.arrivalInfo ? (
                      <span className="route-card-time-badge" style={{
                        background: 'rgba(0, 242, 254, 0.15)',
                        color: '#00f2fe',
                        padding: '2px 6px',
                        borderRadius: '6px',
                        fontWeight: 'bold',
                        fontSize: '11px',
                        border: '1px solid rgba(0, 242, 254, 0.3)',
                        marginLeft: 'auto'
                      }}>
                        🕒 {(() => {
                          const startMins = (customItinerary?.metadata?.start_time_hour || 9) * 60;
                          const arrMins = startMins + lm.arrivalInfo.arriving_time;
                          const h = Math.floor(arrMins / 60) % 24;
                          const m = Math.round(arrMins % 60);
                          return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
                        })()}
                      </span>
                    ) : (
                      <span>{lm.rating.toFixed(1)} ★</span>
                    )}
                  </div>
                </div>
              </article>
            ))}
          </div>

          {customItinerary ? (
            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                className="generate-button"
                onClick={() => navigate("/plan")}
                type="button"
                style={{ background: 'rgba(255, 255, 255, 0.08)', border: '1px solid rgba(255, 255, 255, 0.15)', color: '#fff' }}
              >
                🔄 Plan New
              </button>
              <button
                className="generate-button"
                onClick={() => setShowHotels((v) => !v)}
                type="button"
                style={{ flex: 1 }}
              >
                {showHotels ? "Hide Hotels" : "Show Hotels"}
              </button>
            </div>
          ) : (
            <button
              className="generate-button"
              onClick={() => setShowHotels((v) => !v)}
              type="button"
            >
              {showHotels ? "Refresh Route" : "Build Route"}
            </button>
          )}
        </div>
      </aside>

      {/* ═══ MAP ═══ */}
      <main className="map-area">
        <div className="map-ui-overlay">
          <div className="map-quickpanel">
            <p className="map-quickpanel-title">Live route briefing</p>
            <p className="map-quickpanel-text">
              {customItinerary 
                ? `Enjoy your personalized ${customItinerary.metadata?.time_budget_hours}h trip starting at ${customItinerary.hotel} using the optimized ${customItinerary.algorithm} plan.`
                : "Follow a curated itinerary through Algiers with coastal viewpoints, heritage stops, and local dining highlights."}
            </p>
          </div>
        </div>
        

        <MapComponent
          landmarks={displayLandmarks}
          hotels={hotels}
          highlightId={highlightId}
          startingHotel={startHotelIndex}
          destinationHotel={startHotelIndex}
          showHotels={showHotels}
          onMarkerClick={handleMarkerClick}
          onToggleSidebar={handleToggleSidebar}
        />
      </main>
    </div>
  );
}