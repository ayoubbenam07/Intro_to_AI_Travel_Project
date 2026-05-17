/**
 * Chip — selectable tag component.
 *
 * Props:
 *   label     – text to display
 *   selected  – boolean
 *   onClick   – callback
 *   icon      – optional emoji / ReactNode shown before label
 */
export default function Chip({ label, selected = false, onClick, icon }) {
  return (
    <button
      type="button"
      className={`chip-ds ${selected ? "chip-ds--selected" : ""}`}
      onClick={onClick}
    >
      {icon && <span className="chip-ds__icon">{icon}</span>}
      <span>{label}</span>
    </button>
  );
}
