import SearchBox from "../components/SearchBox";
import { FaBed } from "react-icons/fa";

/**
 * HotelPhase — Departure hotel search and selection.
 *
 * Props:
 *   hotels   – full hotel array (loaded externally)
 *   selected – currently selected hotel object or null
 *   onChange – (hotel) => void
 */
export default function HotelPhase({ hotels, selected, onChange }) {
  return (
    <div className="plan-phase" key="hotel">
      <h2 className="plan-phase__heading">Departure Hotel</h2>
      <p className="plan-phase__desc">
        Where will you start your journey? Search for your hotel below.
      </p>

      <label className="plan-label">Hotel</label>
      <SearchBox
        items={hotels}
        value={selected}
        onChange={onChange}
        placeholder="e.g. Sofitel Algiers Hamma Garden"
        getLabel={(h) => h.name}
      />

      {selected && (
        <div
          style={{
            marginTop: 16,
            padding: "12px 16px",
            borderRadius: 12,
            background: "rgba(0, 119, 190, 0.1)",
            border: "1px solid rgba(0, 119, 190, 0.25)",
            display: "flex",
            alignItems: "center",
            gap: 10,
          }}
        >
          <FaBed size={20} style={{ color: "var(--color-primary)", flexShrink: 0 }} />
          <div>
            <div
              style={{
                fontFamily: "var(--font-body)",
                fontSize: "var(--text-sm)",
                fontWeight: 600,
                color: "var(--color-neutral-1000)",
              }}
            >
              {selected.name}
            </div>
            <div
              style={{
                fontFamily: "var(--font-body)",
                fontSize: "var(--text-xs)",
                color: "var(--color-neutral-500)",
              }}
            >
              {selected.latitude.toFixed(4)}°N, {selected.longitude.toFixed(4)}°E
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
