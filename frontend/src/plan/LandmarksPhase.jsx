import { useState } from "react";
import Chip from "../components/Chip";

const LANDMARK_TYPES = [
  { key: "Monument", icon: "🏛️" },
  { key: "Nature", icon: "🌿" },
  { key: "Historical Site", icon: "🏰" },
  { key: "Mosque", icon: "🕌" },
  { key: "Cathedral", icon: "⛪" },
  { key: "Museum", icon: "🎨" },
  { key: "Cultural Center & Event Venue", icon: "🎭" },
  { key: "Park", icon: "🌳" },
  { key: "Public Square", icon: "📍" },
  { key: "Beach", icon: "🏖️" },
  { key: "Shopping/Mall", icon: "🛍️" },
];

/**
 * LandmarksPhase — Preferred landmark types.
 */
export default function LandmarksPhase({ selectedTypes, onChange }) {
  const [mode, setMode] = useState(
    selectedTypes.length === LANDMARK_TYPES.length ? "all" : "custom"
  );

  function handleModeSwitch(m) {
    setMode(m);
    if (m === "all") onChange(LANDMARK_TYPES.map((t) => t.key));
  }

  function toggleType(key) {
    if (selectedTypes.includes(key)) {
      const next = selectedTypes.filter((t) => t !== key);
      onChange(next.length === 0 ? [key] : next); // keep at least one
    } else {
      onChange([...selectedTypes, key]);
    }
  }

  return (
    <div className="plan-phase" key="landmarks">
      <h2 className="plan-phase__heading">Landmarks</h2>
      <p className="plan-phase__desc">
        Which types of places interest you most?
      </p>

      <div className="landmark-toggle">
        <button
          type="button"
          className={`landmark-toggle__btn ${mode === "all" ? "landmark-toggle__btn--active" : ""}`}
          onClick={() => handleModeSwitch("all")}
        >
          All Types
        </button>
        <button
          type="button"
          className={`landmark-toggle__btn ${mode === "custom" ? "landmark-toggle__btn--active" : ""}`}
          onClick={() => setMode("custom")}
        >
          Custom Selection
        </button>
      </div>

      {mode === "custom" && (
        <div className="plan-chips">
          {LANDMARK_TYPES.map((t) => (
            <Chip
              key={t.key}
              label={t.key}
              icon={t.icon}
              selected={selectedTypes.includes(t.key)}
              onClick={() => toggleType(t.key)}
            />
          ))}
        </div>
      )}

      {mode === "all" && (
        <div style={{ padding: "12px 16px", borderRadius: 12, background: "rgba(0,119,190,0.06)", border: "1px solid rgba(0,119,190,0.15)", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 18 }}>✨</span>
          <span style={{ fontFamily: "var(--font-body)", fontSize: "var(--text-sm)", color: "var(--color-neutral-600)" }}>
            All {LANDMARK_TYPES.length} landmark types will be considered.
          </span>
        </div>
      )}
    </div>
  );
}

export { LANDMARK_TYPES };
