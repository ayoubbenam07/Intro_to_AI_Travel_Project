import React, { useEffect, useState, useCallback, useMemo, useRef } from "react";
import { useLocation } from "react-router-dom";
import MapComponent from "../map/MapComponent.jsx";
import { loadLandmarks, loadHotels, getTypeColor, getTypeIcon } from "../map/data.js";
import "./Itinerary.css";

export default function Itinerary({ 
  startingHotel: propStartingHotel, 
  destinationHotel: propDestinationHotel, 
  landmarkIDs: propLandmarkIDs 
} = {}) {
  const location = useLocation();
  const state = location.state || {};

  // Extract user selections
  const budget = state.budget ?? 12; // default 12 hrs
  const selectedHotel = state.hotel ?? 1; // default 1st hotel
  const landmarkTypes = state.landmarkTypes ?? [];
  const algorithm = state.algorithm ?? "greedy";

  const [landmarks, setLandmarks] = useState([]);
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [highlightId, setHighlightId] = useState(null);
  const [mapExpanded, setMapExpanded] = useState(false);
  const [detailLandmark, setDetailLandmark] = useState(null);

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

  /* ── Dynamic Planning Engine ── */
  const { orderedLandmarks, totalTime } = useMemo(() => {
    if (!landmarks?.length) return { orderedLandmarks: [], totalTime: 0 };

    // 1. Explicit IDs via props (e.g. from static demo)
    if (propLandmarkIDs?.length) {
      const ordered = propLandmarkIDs.map(id => landmarks.find(l => l.id === id)).filter(Boolean);
      const total = ordered.reduce((sum, lm) => sum + (lm.estimatedTime || 0), 0);
      return { orderedLandmarks: ordered, totalTime: total };
    }

    // 2. Dynamic client-side greedy travel algorithm
    let filtered = landmarks;
    if (landmarkTypes && landmarkTypes.length > 0) {
      filtered = landmarks.filter(lm => landmarkTypes.includes(lm.type));
    }

    // Sort by rating desc to prioritize high interest spots
    const sorted = [...filtered].sort((a, b) => b.rating - a.rating);

    const budgetMinutes = budget * 60;
    let accumulatedTime = 0;
    const selected = [];

    for (const lm of sorted) {
      const visitTime = lm.estimatedTime || 45;
      if (accumulatedTime + visitTime <= budgetMinutes) {
        selected.push(lm);
        accumulatedTime += visitTime;
      }
    }

    // Fallback if no matching landmarks found (default Casbah adventure)
    if (selected.length === 0) {
      const fallbackIds = [1, 24, 31, 51, 10, 8, 23, 42, 37, 16, 12, 40, 21, 9, 45];
      const ordered = fallbackIds.map(id => landmarks.find(l => l.id === id)).filter(Boolean);
      const total = ordered.reduce((sum, lm) => sum + (lm.estimatedTime || 0), 0);
      return { orderedLandmarks: ordered, totalTime: total };
    }

    return { orderedLandmarks: selected, totalTime: accumulatedTime };
  }, [landmarks, propLandmarkIDs, landmarkTypes, budget]);

  const startingHotel = propStartingHotel ?? selectedHotel;
  const destinationHotel = propDestinationHotel ?? selectedHotel;

  /* ── Cumulative time for each stop ── */
  const cumulativeTimes = useMemo(() => {
    let total = 0;
    return orderedLandmarks.map((lm) => {
      total += lm.estimatedTime || 0;
      return total;
    });
  }, [orderedLandmarks]);

  /* ── Slider logic: show 2 items at a time ── */
  const slidesPerView = 2;
  const maxSlide = Math.max(0, orderedLandmarks.length - slidesPerView);

  const handlePrev = useCallback(() => {
    setCurrentSlide((s) => Math.max(0, s - 1));
  }, []);

  const handleNext = useCallback(() => {
    setCurrentSlide((s) => Math.min(maxSlide, s + 1));
  }, [maxSlide]);

  /* ── Highlight & map interaction ── */
  const handleCardClick = useCallback((lm) => {
    setHighlightId(lm.id);
  }, []);

  const handleMarkerClick = useCallback((lm) => {
    setHighlightId(lm.id);
    // Find the index of this landmark & scroll slider to it
    const idx = orderedLandmarks.findIndex((l) => l.id === lm.id);
    if (idx >= 0) {
      setCurrentSlide(Math.min(idx, maxSlide));
    }
  }, [orderedLandmarks, maxSlide]);

  /* ── Toggle fullscreen map ── */
  const toggleMapFullscreen = useCallback(() => {
    setMapExpanded((v) => {
      const next = !v;
      // Lock/unlock body scroll
      document.body.style.overflow = next ? "hidden" : "";
      // Invalidate leaflet map size after the CSS transition
      setTimeout(() => {
        window.dispatchEvent(new Event("resize"));
      }, 450);
      return next;
    });
  }, []);

  /* ── Close fullscreen / modal on Escape ── */
  useEffect(() => {
    const handler = (e) => {
      if (e.key === "Escape") {
        if (detailLandmark) {
          setDetailLandmark(null);
        } else if (mapExpanded) {
          setMapExpanded(false);
          document.body.style.overflow = "";
          setTimeout(() => window.dispatchEvent(new Event("resize")), 450);
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [mapExpanded, detailLandmark]);

  /* ── Visible landmarks in the current slide window ── */
  const visibleLandmarks = orderedLandmarks.slice(
    currentSlide,
    currentSlide + slidesPerView
  );

  if (loading) {
    return (
      <div className="itin-loader">
        <div className="itin-loader__spinner" />
        <p>Preparing your itinerary…</p>
      </div>
    );
  }

  return (
    <div className="itin-page">
      {/* ═══ HEADER ═══ */}
      <header className="itin-header">
        <span className="itin-eyebrow">Your Itinerary</span>
        <h1 className="itin-title">Explore Algiers, step by step.</h1>
        <p className="itin-subtitle">
          {orderedLandmarks.length} landmarks · ~{totalTime} min total ·
          AI-optimised route
        </p>
      </header>

      {/* ═══ PROGRESS BAR ═══ */}
      <div className="itin-progress-wrap">
        <div className="itin-progress-bar">
          <div
            className="itin-progress-fill"
            style={{
              width: `${((currentSlide + slidesPerView) / orderedLandmarks.length) * 100}%`,
            }}
          />
        </div>
        <span className="itin-progress-label">
          Stop {currentSlide + 1}–
          {Math.min(currentSlide + slidesPerView, orderedLandmarks.length)} of{" "}
          {orderedLandmarks.length}
        </span>
      </div>

      {/* ═══ SLIDER ═══ */}
      <section className="itin-slider-section">
        <button
          className="itin-arrow itin-arrow--left"
          onClick={handlePrev}
          disabled={currentSlide === 0}
          aria-label="Previous landmarks"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>

        <div className="itin-slider-track">
          {visibleLandmarks.map((lm, i) => {
            const globalIndex = currentSlide + i;
            const cumTime = cumulativeTimes[globalIndex] || 0;
            const color = getTypeColor(lm.type);
            const icon = getTypeIcon(lm.type);
            const isActive = highlightId === lm.id;

            return (
              <article
                key={lm.id}
                className={`itin-card ${isActive ? "itin-card--active" : ""}`}
                onClick={() => handleCardClick(lm)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === "Enter" && handleCardClick(lm)}
              >
                {/* Step badge */}
                <div className="itin-card__step">
                  <span className="itin-card__step-num">{globalIndex + 1}</span>
                </div>

                {/* Icon */}
                <div
                  className="itin-card__icon"
                  style={{
                    background: `linear-gradient(135deg, ${color}, ${color}bb)`,
                  }}
                >
                  {icon}
                </div>

                {/* Body */}
                <div className="itin-card__body">
                  <h3 className="itin-card__name">{lm.name}</h3>
                  <div className="itin-card__meta">
                    <span className="itin-card__chip">{lm.type}</span>
                    <span className="itin-card__rating">
                      ★ {lm.rating.toFixed(1)}
                    </span>
                  </div>
                  <p className="itin-card__desc">
                    {lm.description?.slice(0, 100)}
                    {lm.description?.length > 100 ? "…" : ""}
                  </p>
                </div>

                {/* Time block */}
                <div className="itin-card__time-block">
                  <span className="itin-card__time-icon">⏱</span>
                  <span className="itin-card__time-val">
                    {lm.estimatedTime} min
                  </span>
                  <span className="itin-card__time-cum">
                    {cumTime} min elapsed
                  </span>
                </div>

                {/* More Details button */}
                <button
                  className="itin-card__details-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    setDetailLandmark(lm);
                  }}
                >
                  More Details
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="9 18 15 12 9 6" />
                  </svg>
                </button>
              </article>
            );
          })}
        </div>

        <button
          className="itin-arrow itin-arrow--right"
          onClick={handleNext}
          disabled={currentSlide >= maxSlide}
          aria-label="Next landmarks"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
      </section>

      {/* ── Dot indicators ── */}
      <div className="itin-dots">
        {orderedLandmarks.map((_, i) => (
          <button
            key={i}
            className={`itin-dot ${i >= currentSlide && i < currentSlide + slidesPerView
                ? "itin-dot--active"
                : ""
              }`}
            onClick={() => setCurrentSlide(Math.min(i, maxSlide))}
            aria-label={`Go to stop ${i + 1}`}
          />
        ))}
      </div>

      {/* ═══ MAP SECTION ═══ */}
      <section
        className={`itin-map-section ${mapExpanded ? "itin-map-section--fullscreen" : ""}`}
      >
        {/* Map toolbar */}
        <div className="itin-map-toolbar">
          <div className="itin-map-toolbar__left">
            <span className="itin-map-toolbar__icon">🗺️</span>
            <span className="itin-map-toolbar__label">Route Map</span>
          </div>
          <button
            className="itin-map-toolbar__expand"
            onClick={toggleMapFullscreen}
            aria-label={mapExpanded ? "Exit fullscreen" : "Expand map"}
          >
            {mapExpanded ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="4 14 10 14 10 20" />
                <polyline points="20 10 14 10 14 4" />
                <line x1="14" y1="10" x2="21" y2="3" />
                <line x1="3" y1="21" x2="10" y2="14" />
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="15 3 21 3 21 9" />
                <polyline points="9 21 3 21 3 15" />
                <line x1="21" y1="3" x2="14" y2="10" />
                <line x1="3" y1="21" x2="10" y2="14" />
              </svg>
            )}
            <span>{mapExpanded ? "Minimize" : "Fullscreen"}</span>
          </button>
        </div>

        {/* Map container */}
        <div className="itin-map-container">
          <MapComponent
            landmarks={orderedLandmarks}
            hotels={hotels}
            highlightId={highlightId}
            startingHotel={startingHotel}
            destinationHotel={destinationHotel}
            showHotels={false}       
            onMarkerClick={handleMarkerClick}
            onToggleSidebar={() => { }}
            style={{ minHeight: "100%", borderRadius: 0 }}
          />
        </div>
      </section>

      {/* ═══ DETAIL MODAL ═══ */}
      {detailLandmark && (
        <DetailModal
          landmark={detailLandmark}
          onClose={() => setDetailLandmark(null)}
        />
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════
   HELPERS
   ═══════════════════════════════════════════════════════ */

const DAY_LABELS = [
  { key: "mon", label: "Mon" },
  { key: "tue", label: "Tue" },
  { key: "wed", label: "Wed" },
  { key: "thu", label: "Thu" },
  { key: "fri", label: "Fri" },
  { key: "sat", label: "Sat" },
  { key: "sun", label: "Sun" },
];

/** Convert a 24-element binary array into a human-readable range string, e.g. "09:00 – 19:00" */
function formatHoursRange(arr) {
  if (!arr || !Array.isArray(arr)) return "Closed";
  const open = arr.indexOf(1);
  const close = arr.lastIndexOf(1);
  if (open === -1) return "Closed";
  if (open === 0 && close === 23) return "Open 24h";
  return `${String(open).padStart(2, "0")}:00 – ${String(close + 1).padStart(2, "0")}:00`;
}

/* ═══════════════════════════════════════════════════════
   DETAIL MODAL
   ═══════════════════════════════════════════════════════ */

function DetailModal({ landmark, onClose }) {
  const lm = landmark;
  const color = getTypeColor(lm.type);
  const icon = getTypeIcon(lm.type);
  const pct = Math.min((lm.rating / 10) * 100, 100);

  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = ""; };
  }, []);

  return (
    <div className="itin-modal-overlay" onClick={onClose}>
      <div
        className="itin-modal"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label={`Details for ${lm.name}`}
      >
        {/* Close button */}
        <button className="itin-modal__close" onClick={onClose} aria-label="Close">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        {/* Header */}
        <div
          className="itin-modal__header"
          style={{ background: `linear-gradient(135deg, ${color}, ${color}cc)` }}
        >
          <span className="itin-modal__header-icon">{icon}</span>
          <div>
            <h2 className="itin-modal__title">{lm.name}</h2>
            <span className="itin-modal__type-badge">{lm.type}</span>
          </div>
        </div>

        {/* Body */}
        <div className="itin-modal__body">
          {/* Description */}
          <div className="itin-modal__section">
            <h4 className="itin-modal__section-title">Description</h4>
            <p className="itin-modal__desc">{lm.description}</p>
          </div>

          {/* Stats row */}
          <div className="itin-modal__stats">
            <div className="itin-modal__stat">
              <span className="itin-modal__stat-label">Rating</span>
              <div className="itin-modal__stat-rating">
                <span className="itin-modal__stat-val" style={{ color }}>★ {lm.rating.toFixed(1)}</span>
                <div className="itin-modal__rating-bar">
                  <div
                    className="itin-modal__rating-fill"
                    style={{ width: `${pct}%`, background: `linear-gradient(90deg, ${color}, ${color}cc)` }}
                  />
                </div>
              </div>
            </div>
            <div className="itin-modal__stat">
              <span className="itin-modal__stat-label">Est. Visit</span>
              <span className="itin-modal__stat-val itin-modal__stat-val--big">⏱ {lm.estimatedTime} min</span>
            </div>
            <div className="itin-modal__stat">
              <span className="itin-modal__stat-label">Coordinates</span>
              <span className="itin-modal__stat-val itin-modal__stat-val--mono">
                {lm.latitude.toFixed(4)}, {lm.longitude.toFixed(4)}
              </span>
            </div>
          </div>

          {/* Opening Hours */}
          <div className="itin-modal__section">
            <h4 className="itin-modal__section-title">Opening Hours</h4>
            {lm.hours ? (
              <div className="itin-modal__hours-grid">
                {DAY_LABELS.map(({ key, label }) => {
                  const dayArr = lm.hours[key];
                  const rangeStr = formatHoursRange(dayArr);
                  const isOpen = rangeStr !== "Closed";
                  return (
                    <div
                      key={key}
                      className={`itin-modal__hours-row ${isOpen ? "" : "itin-modal__hours-row--closed"}`}
                    >
                      <span className="itin-modal__hours-day">{label}</span>
                      <span className="itin-modal__hours-range">{rangeStr}</span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="itin-modal__no-data">Hours data not available</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
