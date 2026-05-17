/**
 * BudgetPhase — Time budget selection (1–24 hours).
 */
export default function BudgetPhase({ budget, onChange }) {
  return (
    <div className="plan-phase" key="budget">
      <h2 className="plan-phase__heading">Time Budget</h2>
      <p className="plan-phase__desc">
        How many hours do you have for your Algiers journey?
      </p>

      <div className="budget-display">
        <span className="budget-display__number">{budget}</span>
        <span className="budget-display__unit">
          {budget === 1 ? "hour" : "hours"}
        </span>
      </div>

      <input
        type="range"
        className="plan-slider"
        min={1}
        max={24}
        step={1}
        value={budget}
        onChange={(e) => onChange(Number(e.target.value))}
        style={{
          background: `linear-gradient(to right, var(--color-primary) ${
            ((budget - 1) / 23) * 100
          }%, #E4E7EB ${((budget - 1) / 23) * 100}%)`,
        }}
      />

      <div className="budget-range-labels">
        <span>1h</span>
        <span>6h</span>
        <span>12h</span>
        <span>18h</span>
        <span>24h</span>
      </div>
    </div>
  );
}
