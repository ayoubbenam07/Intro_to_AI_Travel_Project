import { useState } from "react";
import Chip from "../components/Chip";
import { getTypeIcon } from "../map/data.js";

const LANDMARK_TYPES = [
  { key: "Monument" },
  { key: "Nature" },
  { key: "Historical Site" },
  { key: "Mosque" },
  { key: "Cathedral" },
  { key: "Museum" },
  { key: "Cultural Center & Event Venue" },
  { key: "Park" },
  { key: "Public Square" },
  { key: "Beach" },
  { key: "Shopping/Mall" },
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
            icon={getTypeIcon(t.key)}
            selected={selectedTypes.includes(t.key)}
            onClick={() => toggleType(t.key)}
          />
        ))}
      </div>
    </div>
  );
}

export { LANDMARK_TYPES };
