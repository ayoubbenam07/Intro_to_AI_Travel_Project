import React, { useEffect, useState, useCallback, useMemo, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MapComponent from "../map/MapComponent.jsx";
import { loadHotels, getTypeColor, getTypeIcon } from "../map/data.js";
import "./Itinerary.css";

export default function Itinerary({ 
  startingHotel: propStartingHotel, 
  destinationHotel: propDestinationHotel, 
  landmarkIDs: propLandmarkIDs 
} = {}) {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state || {};

  // Extract user selections
  const budget = state.budget ?? 12; // default 12 hrs
  const selectedHotel = state.hotel ?? 1; // default 1st hotel
  const landmarkTypes = state.landmarkTypes ?? [];
  const algorithm = state.algorithm ?? "greedy";

  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [highlightId, setHighlightId] = useState(null);
  const [mapExpanded, setMapExpanded] = useState(false);
  const [detailLandmark, setDetailLandmark] = useState(null);
  
  const [historicalPath, setHistoricalPath] = useState(null);
  const [emptyState, setEmptyState] = useState(false);
  const [isLatestFallback, setIsLatestFallback] = useState(false);

  /* ── Load data ── */
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Load base context data
        // Load hotel data for map markers
        const ht = await loadHotels();
        setHotels(ht);

        const token = localStorage.getItem("token");

        // 1. If we are viewing a historical itinerary (explicit ID)
        if (state.itineraryId) {
          const res = await fetch(`http://localhost:8000/api/itineraries/${state.itineraryId}`, {
            headers: {
              "Authorization": `Bearer ${token}`
            }
          });
          if (res.ok) {
            const data = await res.json();
            // Map the backend format to the expected frontend schema
            const mappedPath = data.map(item => ({
              id: item.landmark_id,
              name: item.name,
              type: item.landmark_type,
              latitude: item.lat,
              longitude: item.lon,
              estimatedTime: item.visit_duration || 45,
              images: item.image_url,
              description: item.description,
              rating: item.interest_score || 0,
              icon: getTypeIcon(item.landmark_type),
              color: getTypeColor(item.landmark_type)
            }));
            setHistoricalPath(mappedPath);
          } else {
            console.error("Failed to load historical itinerary details:", res.status);
            setEmptyState(true);
          }
        }
        // 2. If we received a newly generated plan from PlanJourney
        else if (state.itinerary && state.itinerary.path) {
          setHistoricalPath(state.itinerary.path.map(item => ({
            id: item.landmark_id || item.id,
            name: item.name,
            type: item.landmark_type || item.type,
            latitude: item.lat || item.latitude,
            longitude: item.lon || item.longitude,
            estimatedTime: item.visit_duration || item.estimatedTime || 45,
            images: item.image_url || item.images,
            description: item.description,
            rating: item.interest_score || item.rating || 0,
            icon: getTypeIcon(item.landmark_type || item.type),
            color: getTypeColor(item.landmark_type || item.type)
          })));
        }
        // 3. We didn't explicitly request one, so let's try to load the latest
        else if (token && !propLandmarkIDs?.length) {
          const res = await fetch(`http://localhost:8000/api/itineraries`, {
            headers: { "Authorization": `Bearer ${token}` }
          });
          if (res.ok) {
            const list = await res.json();
            if (list && list.length > 0) {
              const latest = list[0]; // The backend returns created_at.desc(), so index 0 is newest
              const pathRes = await fetch(`http://localhost:8000/api/itineraries/${latest.itinerary_id}`, {
                headers: { "Authorization": `Bearer ${token}` }
              });
              
              if (pathRes.ok) {
                const data = await pathRes.json();
                const mappedPath = data.map(item => ({
                  id: item.landmark_id,
                  name: item.name,
                  type: item.landmark_type,
                  latitude: item.lat,
                  longitude: item.lon,
                  estimatedTime: item.visit_duration || 45,
                  images: item.image_url,
                  description: item.description,
                  rating: item.interest_score || 0,
                  icon: getTypeIcon(item.landmark_type),
                  color: getTypeColor(item.landmark_type)
                }));
                setHistoricalPath(mappedPath);
                setIsLatestFallback(true);
              } else {
                setEmptyState(true);
              }
            } else {
              setEmptyState(true);
            }
          } else {
            setEmptyState(true);
          }
        } else if (!propLandmarkIDs?.length) {
          // Not logged in, no state passed
          setEmptyState(true);
        }

      } catch (err) {
        console.error("Error loading itinerary data:", err);
        setEmptyState(true);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [state.itineraryId, state.itinerary, propLandmarkIDs]); // Run once when route loads

  /* ── Dynamic Planning Engine ── */
  const { orderedLandmarks, totalTime } = useMemo(() => {
    // 1. Explicit IDs via props (e.g. from static demo)
    if (propLandmarkIDs?.length && historicalPath) {
      // Demo not fully supported in pure DB mode unless historicalPath is populated manually
    }

    // 2. Load historical itinerary if fetched
    if (historicalPath) {
      const total = historicalPath.reduce((sum, lm) => sum + (lm.estimatedTime || 0), 0);
      return { orderedLandmarks: historicalPath, totalTime: total };
    }

    return { orderedLandmarks: [], totalTime: 0 };
  }, [historicalPath, propLandmarkIDs]);

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

  return (
    <div className="itin-page">

      {/* ═══ HERO BANNER (Profile/Plan-style fade) ═══ */}
      <section className="itin-hero">
        <img
          src="/images/background_image1.jpg"
          alt="Algiers panorama"
          className="itin-hero__img"
          loading="eager"
        />
        <div className="itin-hero__gradient" />
        <div className="itin-hero__content">
          <div className="itin-hero__inner">
            <div className="itin-eyebrow-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '16px' }}>
              <span className="itin-eyebrow" style={{ margin: 0, background: 'var(--bg)', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}>Your Itinerary</span>
              {isLatestFallback && (
                <span className="itin-latest-badge" style={{ 
                  background: 'var(--color-primary)', 
                  padding: '6px 12px', 
                  borderRadius: '20px', 
                  fontSize: '0.75rem', 
                  fontWeight: '700', 
                  letterSpacing: '0.05em', 
                  textTransform: 'uppercase', 
                  color: 'white',
                  boxShadow: '0 4px 12px rgba(0, 119, 190, 0.3)',
                  border: '1px solid rgba(255,255,255,0.2)'
                }}>
                  Latest Generated
                </span>
              )}
            </div>
            <h1 className="itin-title">Explore Algiers, step by step.</h1>
            {!loading && !emptyState && (
              <p className="itin-subtitle">
                {orderedLandmarks.length} landmarks · ~{totalTime} min total ·
                AI-optimised route
              </p>
            )}
          </div>
        </div>
      </section>

      {/* ═══ MAIN CONTENT ═══ */}
      <div className="itin-content">

      {loading ? (
        <div className="itin-loader">
          <div className="itin-loader__spinner" />
          <p>Preparing your itinerary…</p>
        </div>
      ) : emptyState ? (
        <div className="itin-empty-state">
          <div className="itin-empty-state__icon">🗺️</div>
          <h2 className="itin-empty-state__title">No Itinerary Found</h2>
          <p className="itin-empty-state__desc">
            You haven't planned any trips yet. Start a new journey to discover the beauty of Algiers!
          </p>
          <button className="itin-empty-state__btn" onClick={() => navigate("/plan")}>
            Start a Journey
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        </div>
      ) : (
      <>

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
                      ★ {typeof lm.rating === 'number' ? lm.rating.toFixed(1) : (parseFloat(lm.rating) || 0).toFixed(1)}
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

      </>
      )}
      </div>{/* end .itin-content */}

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


        </div>
      </div>
    </div>
  );
}
