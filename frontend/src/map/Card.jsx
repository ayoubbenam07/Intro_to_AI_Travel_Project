import React from "react";

const card = {
  width: "100%",
  borderRadius: 14,
  overflow: "hidden",
  background: "#ffffff",
  boxShadow: "0 8px 30px rgba(0,0,0,.12)",
  fontFamily: "'Inter', system-ui, sans-serif",
  color: "#1e1e2f",
  transition: "transform .25s ease, box-shadow .25s ease",
};

const badgeStyle = (color) => ({
  display: "inline-flex",
  alignItems: "center",
  gap: 5,
  padding: "3px 10px",
  borderRadius: 20,
  fontSize: 11,
  fontWeight: 600,
  letterSpacing: 0.3,
  color: "#fff",
  background: color,
  textTransform: "uppercase",
});

const ratingBarStyle = {
  height: 4,
  borderRadius: 4,
  background: "rgba(0,0,0,.06)",
  overflow: "hidden",
  flex: 1,
};

const ratingFillStyle = (pct, color) => ({
  width: pct + "%",
  height: "100%",
  borderRadius: 4,
  background: "linear-gradient(90deg, " + color + ", " + color + "cc)",
  transition: "width .6s ease",
});

const metaRowStyle = {
  display: "flex",
  alignItems: "center",
  gap: 6,
  fontSize: 12,
  color: "#888",
};

export default function Card({ landmark, compact, onClick }) {
  if (!landmark) return null;

  var id = landmark.id;
  var name = landmark.name;
  var description = landmark.description;
  var type = landmark.type;
  var rating = landmark.rating;
  var estimatedTime = landmark.estimatedTime;
  var icon = landmark.icon;
  var color = landmark.color;
  var pct = Math.min((rating / 10) * 100, 100);

  if (compact) {
    return (
      <div
        style={Object.assign({}, card, {
          width: 220,
          cursor: "default",
          background: "transparent",
          boxShadow: "none",
          borderRadius: 0,
          overflow: "visible",
        })}
        id={"card-" + id}
      >
        <div style={{ background: "linear-gradient(135deg, " + color + ", " + color + "cc)", padding: "10px 14px", display: "flex", alignItems: "center", gap: 8, borderRadius: 12 }}>
          <span style={{ fontSize: 20 }}>{icon}</span>
          <span style={{ fontSize: 13, fontWeight: 700, color: "#fff", lineHeight: 1.25 }}>{name}</span>
        </div>
        <div style={{ padding: "10px 14px 14px" }}>
          <div style={Object.assign({}, metaRowStyle, { marginBottom: 6 })}>
            <span style={{ fontWeight: 700, color: color, fontSize: 13 }}>{"★ " + rating.toFixed(1)}</span>
            <div style={ratingBarStyle}>
              <div style={ratingFillStyle(pct, color)} />
            </div>
          </div>
          <div style={metaRowStyle}>
            <span style={badgeStyle(color)}>{type}</span>
          </div>
          {estimatedTime > 0 && (
            <div style={Object.assign({}, metaRowStyle, { marginTop: 6 })}>
              <span>⏱</span>
              <span>{estimatedTime + " min"}</span>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div
      id={"card-" + id}
      style={card}
      className="landmark-card"
      onClick={function () { if (onClick) onClick(landmark); }}
      role="button"
      tabIndex={0}
      onKeyDown={function (e) { if (e.key === "Enter" && onClick) onClick(landmark); }}
    >
      <div
        style={{
          background: "linear-gradient(135deg, " + color + ", " + color + "aa)",
          padding: "18px 20px 14px",
          display: "flex",
          alignItems: "flex-start",
          gap: 10,
        }}
      >
        <span style={{ fontSize: 28, lineHeight: 1 }}>{icon}</span>
        <div style={{ flex: 1 }}>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700, color: "#fff", lineHeight: 1.3 }}>{name}</h3>
          <div style={{ marginTop: 4 }}>
            <span style={badgeStyle("rgba(255,255,255,.25)")}>{type}</span>
          </div>
        </div>
      </div>
      <div style={{ padding: "14px 20px 18px" }}>
        <p style={{ margin: "0 0 12px", fontSize: 12.5, lineHeight: 1.55, color: "#555" }}>
          {description}
        </p>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
          <span style={{ fontSize: 13, fontWeight: 700, color: color }}>{"★ " + rating.toFixed(1)}</span>
          <div style={ratingBarStyle}>
            <div style={ratingFillStyle(pct, color)} />
          </div>
        </div>
        {estimatedTime > 0 && (
          <div style={metaRowStyle}>
            <span>⏱</span>
            <span>{"~" + estimatedTime + " min visit"}</span>
          </div>
        )}
        <div style={Object.assign({}, metaRowStyle, { marginTop: 6, justifyContent: "flex-end" })}>
          <span style={{ fontSize: 10, background: "#f0f0f5", borderRadius: 4, padding: "2px 6px", color: "#aaa" }}>
            {"ID: " + id}
          </span>
        </div>
      </div>
    </div>
  );
}
