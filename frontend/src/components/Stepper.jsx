/**
 * Stepper — horizontal phase indicator.
 *
 * Props:
 *   steps        – array of { label } objects
 *   currentStep  – 0-based index
 *   onStepClick  – (index) => void  (optional, for clickable steps)
 */
export default function Stepper({ steps = [], currentStep = 0, onStepClick }) {
  return (
    <div className="stepper">
      {steps.map((step, i) => {
        const state =
          i < currentStep ? "completed" : i === currentStep ? "active" : "upcoming";
        return (
          <div key={i} className="stepper__item-wrapper">
            {/* connector line before this dot (skip first) */}
            {i > 0 && (
              <div
                className={`stepper__line ${
                  i <= currentStep ? "stepper__line--filled" : ""
                }`}
              />
            )}

            <button
              type="button"
              className={`stepper__dot stepper__dot--${state}`}
              onClick={() => onStepClick?.(i)}
              aria-label={step.label}
            >
              {state === "completed" ? (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              ) : (
                <span className="stepper__number">{i + 1}</span>
              )}
            </button>

            <span
              className={`stepper__label stepper__label--${state}`}
            >
              {step.label}
            </span>
          </div>
        );
      })}
    </div>
  );
}
