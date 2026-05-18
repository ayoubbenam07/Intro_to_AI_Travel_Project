import Input from "../components/Input";

/**
 * DatePhase — Journey date + starting time.
 */
export default function DatePhase({
  date, startHour, startMinute,
  onDateChange, onHourChange, onMinuteChange,
}) {
  const today = new Date().toISOString().split("T")[0];

  return (
    <div className="plan-phase" key="date">
      <h2 className="plan-phase__heading">Date &amp; Time</h2>
      <p className="plan-phase__desc">
        When will you start exploring? Pick a date and your departure time.
      </p>

      <div className="plan-row" style={{ marginBottom: 20 }}>
        <div>
          <Input
            label="Journey Date"
            type="date"
            value={date}
            min={today}
            onChange={(e) => onDateChange(e.target.value)}
            inputClassName="plan-input-white"
          />
        </div>
        <div>
          <label className="input-label">Starting Time</label>
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <Input
              type="number"
              min={0} max={23} value={startHour}
              onChange={(e) => onHourChange(Math.max(0, Math.min(23, Number(e.target.value))))}
              placeholder="HH"
              inputClassName="plan-input-white"
              style={{ textAlign: "center" }}
            />
            <span style={{ fontSize: "var(--text-2xl)", color: "var(--color-neutral-400)", fontWeight: 700 }}>:</span>
            <Input
              type="number"
              min={0} max={59} value={startMinute}
              onChange={(e) => onMinuteChange(Math.max(0, Math.min(59, Number(e.target.value))))}
              placeholder="MM"
              inputClassName="plan-input-white"
              style={{ textAlign: "center" }}
            />
          </div>
        </div>
      </div>

      {date && (
        <div style={{ padding: "12px 16px", borderRadius: 12, background: "rgba(0,119,190,0.06)", border: "1px solid rgba(0,119,190,0.15)", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 20 }}>📅</span>
          <span style={{ fontFamily: "var(--font-body)", fontSize: "var(--text-sm)", color: "var(--color-neutral-800)" }}>
            {new Date(date + "T00:00").toLocaleDateString("en-GB", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
            {" at "}
            <strong>{String(startHour).padStart(2, "0")}:{String(startMinute).padStart(2, "0")}</strong>
          </span>
        </div>
      )}
    </div>
  );
}
