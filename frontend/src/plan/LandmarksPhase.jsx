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

      <div className="plan-chips" style={{ marginTop: '24px' }}>
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
    </div>
  );
}

export { LANDMARK_TYPES };
