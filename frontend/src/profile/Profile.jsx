import { useState } from "react";

const itineraries = [
  {
    id: 1,
    image: "https://api.builder.io/api/v1/image/assets/TEMP/1a2835182e9c5f47fc2056524b3010564a5232a4?width=811",
    duration: "3 DAYS • HISTORICAL",
    title: "Shadows of the Casbah",
    tags: ["Architecture", "Gastronomy"],
  },
  {
    id: 2,
    image: "https://api.builder.io/api/v1/image/assets/TEMP/4ea494965d51475b61a4b628991996174c7cf46a?width=811",
    duration: "1 DAY • MARITIME",
    title: "Azure Horizon Escape",
    tags: ["Yachting", "Private Deck"],
  },
  {
    id: 3,
    image: "https://api.builder.io/api/v1/image/assets/TEMP/b6147795f09fa6752c2077308893ed00dbf6f55b?width=811",
    duration: "EVENING • CULINARY",
    title: "The Algiers Table",
    tags: ["Fine Dining", "Fusion"],
  },
];

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500&family=Hanken+Grotesk:wght@400;600;700&display=swap');

  .profile-root {
    min-height: 100vh;
    background: #F9F9F9;
    font-family: 'Hanken Grotesk', sans-serif;
    overflow-x: hidden;
  }

  .garamond { font-family: 'EB Garamond', Georgia, serif; }

  /* ── Hero ── */
  .hero {
    position: relative;
    height: 45vh;
    min-height: 300px;
    overflow: hidden;
  }
  @media (min-width: 1024px) { .hero { height: 400px; } }

  .hero-img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.6;
  }

  .hero-bg-placeholder {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #002366 0%, #005E97 50%, #7DF9FF 100%);
    opacity: 0.15;
  }

  .hero-gradient {
    position: absolute;
    inset: 0;
    background: linear-gradient(0deg, #F9F9F9 0%, rgba(249,249,249,0.10) 38.4%, rgba(249,249,249,0.00) 100%);
  }

  .hero-profile {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 0 20px;
  }
  @media (min-width: 768px) { .hero-profile { padding: 0 80px; } }

  .hero-profile-inner-wrap {
    max-width: 1440px;
    margin: 0 auto;
  }

  .hero-profile-inner {
    display: flex;
    align-items: flex-end;
    gap: 24px;
  }
  @media (min-width: 640px) { .hero-profile-inner { gap: 32px; } }

  .avatar {
    width: 96px; height: 96px;
    flex-shrink: 0;
    border-radius: 50%;
    border: 5px solid #F9F9F9;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    overflow: hidden;
  }
  @media (min-width: 640px) { .avatar { width: 128px; height: 128px; } }
  @media (min-width: 768px) { .avatar { width: 176px; height: 176px; border-width: 7px; } }

  .avatar-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0077be 0%, #002366 100%);
    color: #ffffff;
    font-size: 32px;
    font-weight: 700;
  }
  @media (min-width: 640px) { .avatar-placeholder { font-size: 44px; } }
  @media (min-width: 768px) { .avatar-placeholder { font-size: 56px; } }

  .avatar img { width: 100%; height: 100%; object-fit: cover; }

  .hero-name-block { padding-bottom: 24px; }
  @media (min-width: 768px) { .hero-name-block { padding-bottom: 40px; } }

  .hero-name {
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 28px;
    font-weight: 500;
    color: #1A1C1C;
    line-height: 1.2;
  }
  @media (min-width: 640px) { .hero-name { font-size: 36px; } }
  @media (min-width: 768px) { .hero-name { font-size: 48px; line-height: 56px; } }

  /* ── Main ── */
  .profile-content {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 20px 96px;
    display: flex;
    flex-direction: column;
    gap: 64px;
  }
  @media (min-width: 768px) { .profile-content { padding: 0 80px 96px; } }
  @media (min-width: 1024px) { .profile-content { gap: 96px; } }

  /* ── Section headers ── */
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }

  .section-title {
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 28px;
    font-weight: 500;
    color: #1A1C1C;
    line-height: 1.2;
  }
  @media (min-width: 640px) { .section-title { font-size: 36px; } }
  @media (min-width: 1024px) { .section-title { font-size: 48px; } }

  .ai-badge {
    font-size: 11px;
    font-weight: 700;
    color: #005E97;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    white-space: nowrap;
    flex-shrink: 0;
  }
  @media (min-width: 640px) { .ai-badge { font-size: 12px; } }

  /* ── Bento grid ── */
  .bento-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
  }
  @media (min-width: 640px) {
    .bento-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
  @media (min-width: 1024px) {
    .bento-grid {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 380px;
    }
  }

  .bento-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24px;
    border-radius: 32px;
    border: 1px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.4);
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 50px -12px rgba(0,105,109,0.05);
    min-height: 220px;
  }
  @media (min-width: 768px) { .bento-card { padding: 32px; } }
  @media (min-width: 1024px) { .bento-card { min-height: unset; } }

  .bento-card-wide {
    grid-column: span 1;
  }
  @media (min-width: 640px) { .bento-card-wide { grid-column: span 2; } }
  @media (min-width: 1024px) { .bento-card-wide { grid-column: span 1; } }

  .bento-card-blue {
    border-color: rgba(0,94,151,0.20);
    background: rgba(0,94,151,0.05);
  }

  .stat-number {
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 48px;
    font-weight: 400;
    color: #1A1C1C;
    line-height: 1;
  }
  @media (min-width: 1024px) { .stat-number { font-size: 60px; } }

  .stat-number-sm {
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 36px;
    font-weight: 400;
    color: #1A1C1C;
    line-height: 1.1;
  }

  .stat-unit {
    font-size: 18px;
    color: #707882;
  }

  .stat-label {
    font-size: 12px;
    font-weight: 700;
    color: #404751;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-top: 8px;
  }

  .stat-label-lg {
    font-size: 16px;
    font-weight: 600;
    color: #404751;
    letter-spacing: 1px;
    margin-top: 8px;
  }
  @media (min-width: 1024px) { .stat-label-lg { font-size: 20px; } }

  /* ── Itineraries ── */
  .itineraries-scroll {
    display: flex;
    gap: 24px;
    overflow-x: auto;
    padding-bottom: 24px;
    margin: 0 -20px;
    padding-left: 20px;
    padding-right: 20px;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  .itineraries-scroll::-webkit-scrollbar { display: none; }
  @media (min-width: 768px) {
    .itineraries-scroll {
      gap: 32px;
      margin: 0;
      padding-left: 0;
      padding-right: 0;
    }
  }
  @media (min-width: 1024px) {
    .itineraries-scroll {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 32px;
      margin: 0;
      padding: 0;
      overflow-x: visible;
    }
  }

  .itinerary-card {
    position: relative;
    flex-shrink: 0;
    width: 280px;
    height: 440px;
    border-radius: 40px;
    overflow: hidden;
    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.10), 0 8px 10px -6px rgba(0,0,0,0.10);
    cursor: pointer;
    transition: transform 0.3s ease;
  }
  .itinerary-card:hover { transform: translateY(-6px); }
  @media (min-width: 640px) { .itinerary-card { width: 340px; height: 480px; } }
  @media (min-width: 768px) { .itinerary-card { width: 380px; height: 500px; border-radius: 48px; } }
  @media (min-width: 1024px) {
    .itinerary-card {
      width: 100%;
      max-width: 380px;
      margin: 0 auto;
    }
  }

  .itinerary-card img {
    position: absolute;
    inset: 0;
    width: 100%; height: 100%;
    object-fit: cover;
  }

  .itinerary-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(0deg, rgba(0,94,151,0.60) 0%, rgba(0,94,151,0.00) 100%);
  }

  .itinerary-info {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 28px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  @media (min-width: 768px) { .itinerary-info { padding: 32px; } }

  .itinerary-duration {
    font-size: 11px;
    font-weight: 700;
    color: rgba(255,255,255,0.8);
    letter-spacing: 1.2px;
    text-transform: uppercase;
  }

  .itinerary-title {
    font-family: 'EB Garamond', Georgia, serif;
    font-size: 26px;
    font-weight: 400;
    color: white;
    line-height: 1.2;
  }

  .itinerary-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding-top: 6px;
  }

  .itinerary-tag {
    padding: 4px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.20);
    backdrop-filter: blur(8px);
    font-size: 11px;
    color: white;
  }

  .view-all-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #005E97;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 1px;
    background: none;
    border: none;
    cursor: pointer;
    transition: opacity 0.2s;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .view-all-btn:hover { opacity: 0.7; }
  @media (min-width: 640px) { .view-all-btn { font-size: 18px; } }

  /* ── Preferences panel ── */
  .preferences-panel {
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 40px;
    border-radius: 48px;
    border: 1px solid rgba(255,255,255,0.5);
    background: rgba(255,255,255,0.40);
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.15);
  }
  @media (min-width: 768px) { .preferences-panel { padding: 48px; gap: 48px; border-radius: 64px; } }

  .pref-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    text-align: center;
  }

  .pref-subtitle {
    font-size: 15px;
    color: #404751;
    max-width: 440px;
    line-height: 1.65;
  }

  .pref-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 40px;
  }
  @media (min-width: 768px) {
    .pref-grid {
      grid-template-columns: repeat(3, 1fr);
      gap: 48px;
    }
  }

  .pref-col { display: flex; flex-direction: column; gap: 20px; }

  .pref-col-header {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .pref-col-title {
    font-size: 18px;
    font-weight: 600;
    color: #005E97;
    letter-spacing: 1px;
  }

  /* Budget buttons */
  .budget-list { display: flex; flex-direction: column; gap: 10px; }

  .budget-btn {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    border-radius: 16px;
    border: 1px solid transparent;
    background: rgba(255,255,255,0.4);
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
  }
  .budget-btn.active {
    border-color: #005E97;
    background: rgba(0,94,151,0.08);
    box-shadow: 0 4px 14px rgba(0,105,109,0.08);
  }

  .budget-label {
    font-size: 15px;
    color: #404751;
  }
  .budget-label.active {
    font-weight: 700;
    color: #005E97;
  }

  .radio-dot {
    width: 18px; height: 18px;
    border-radius: 50%;
    border: 1.5px solid #6B7280;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s;
  }
  .radio-dot.active {
    background: #005E97;
    border-color: #005E97;
  }
  .radio-inner {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: white;
  }

  /* Slider */
  .slider-wrap { display: flex; flex-direction: column; gap: 16px; padding-top: 8px; }

  .range-input {
    -webkit-appearance: none;
    width: 100%;
    height: 4px;
    border-radius: 2px;
    background: linear-gradient(to right, #005E97 0%, #005E97 var(--pct, 50%), #D1D8E2 var(--pct, 50%), #D1D8E2 100%);
    outline: none;
    cursor: pointer;
  }
  .range-input::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px; height: 20px;
    border-radius: 50%;
    background: #005E97;
    box-shadow: 0 2px 8px rgba(0,94,151,0.30);
    cursor: pointer;
    transition: transform 0.15s;
  }
  .range-input::-webkit-slider-thumb:hover { transform: scale(1.2); }
  .range-input::-moz-range-thumb {
    width: 20px; height: 20px;
    border-radius: 50%;
    background: #005E97;
    border: none;
    box-shadow: 0 2px 8px rgba(0,94,151,0.30);
    cursor: pointer;
  }

  .slider-labels {
    display: flex;
    justify-content: space-between;
  }
  .slider-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #707882;
    transition: color 0.2s;
  }
  .slider-label.active {
    color: #005E97;
    font-weight: 700;
  }

  .slider-desc {
    font-size: 13px;
    color: #404751;
    line-height: 1.65;
  }

  /* Dietary chips */
  .chips { display: flex; flex-wrap: wrap; gap: 8px; }

  .chip {
    padding: 8px 20px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    border: 1.5px solid #C0C7D2;
    color: #404751;
    background: transparent;
    cursor: pointer;
    transition: all 0.2s;
  }
  .chip.active {
    border-color: #005E97;
    background: rgba(0,94,151,0.06);
    color: #005E97;
  }

  /* Divider between pref cols on mobile */
  .pref-divider {
    display: block;
    height: 1px;
    background: rgba(0,94,151,0.10);
  }
  @media (min-width: 768px) { .pref-divider { display: none; } }

  /* ── Time Budget ── */
  .time-budget-container {
    max-width: 600px;
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    background: rgba(255, 255, 255, 0.45);
    padding: 32px;
    border-radius: 32px;
    border: 1px solid rgba(0, 94, 151, 0.1);
    box-shadow: 0 10px 30px rgba(0, 94, 151, 0.04);
  }

  .time-budget-header {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .time-budget-title {
    font-size: 20px;
    font-weight: 600;
    color: #005E97;
    letter-spacing: 1px;
  }

  .time-budget-display {
    font-size: 64px;
    font-weight: 700;
    color: #1A1C1C;
    line-height: 1;
    display: flex;
    align-items: baseline;
    gap: 8px;
  }

  .time-budget-unit {
    font-size: 24px;
    color: #707882;
    font-weight: 400;
  }
`;

export default function Profile() {
  const [timeBudget, setTimeBudget] = useState(12);

  const sliderPct = `${((timeBudget - 2) / 22) * 100}%`;

  return (
    <>
      <style>{styles}</style>
      <div className="profile-root">

        {/* ── Hero ── */}
        <section className="hero">
          <img
            src="https://api.builder.io/api/v1/image/assets/TEMP/961f41d5192120e61628a2dd3ebe6cd1b4abdd73?width=3250"
            alt=""
            className="hero-img"
          />
          <div className="hero-gradient" />
          <div className="hero-profile">
            <div className="hero-profile-inner-wrap">
              <div className="hero-profile-inner">
                <div className="avatar avatar-placeholder">
                  <span>MG</span>
                </div>
                <div className="hero-name-block" style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  <h1 className="hero-name garamond">Meghabber mohammed Al Ghazali</h1>
                  <button 
                    onClick={() => {
                      localStorage.removeItem("isLoggedIn");
                      localStorage.removeItem("userEmail");
                      window.location.href = "/";
                    }}
                    style={{
                      alignSelf: "flex-start",
                      background: "transparent",
                      border: "none",
                      color: "#c0392b",
                      fontFamily: "var(--font-body)",
                      fontSize: "14px",
                      fontWeight: 600,
                      cursor: "pointer",
                      padding: 0,
                      textTransform: "uppercase",
                      letterSpacing: "1px",
                      transition: "opacity 0.2s"
                    }}
                    onMouseEnter={(e) => e.target.style.opacity = 0.8}
                    onMouseLeave={(e) => e.target.style.opacity = 1}
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Main ── */}
        <main className="profile-content">

          {/* ── Digital Footprint ── */}
          <section style={{ display: "flex", flexDirection: "column", gap: 32 }}>
            <div className="section-header">
              <h2 className="section-title garamond">Digital Footprint</h2>
            </div>

            <div className="bento-grid">
              {/* Wide card */}
              <div className="bento-card bento-card-wide">
                <svg width="27" height="27" viewBox="0 0 27 27" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 27C7.35 27 5.9375 26.4125 4.7625 25.2375C3.5875 24.0625 3 22.65 3 21V8.7375C2.125 8.4125 1.40625 7.86875 0.84375 7.10625C0.28125 6.34375 0 5.475 0 4.5C0 3.25 0.4375 2.1875 1.3125 1.3125C2.1875 0.4375 3.25 0 4.5 0C5.75 0 6.8125 0.4375 7.6875 1.3125C8.5625 2.1875 9 3.25 9 4.5C9 5.475 8.71875 6.34375 8.15625 7.10625C7.59375 7.86875 6.875 8.4125 6 8.7375V21C6 21.825 6.29375 22.5312 6.88125 23.1187C7.46875 23.7062 8.175 24 9 24C9.825 24 10.5312 23.7062 11.1187 23.1187C11.7062 22.5312 12 21.825 12 21V6C12 4.35 12.5875 2.9375 13.7625 1.7625C14.9375 0.5875 16.35 0 18 0C19.65 0 21.0625 0.5875 22.2375 1.7625C23.4125 2.9375 24 4.35 24 6V18.2625C24.875 18.5875 25.5938 19.1312 26.1562 19.8937C26.7188 20.6562 27 21.525 27 22.5C27 23.75 26.5625 24.8125 25.6875 25.6875C24.8125 26.5625 23.75 27 22.5 27C21.25 27 20.1875 26.5625 19.3125 25.6875C18.4375 24.8125 18 23.75 18 22.5C18 21.525 18.2812 20.65 18.8438 19.875C19.4062 19.1 20.125 18.5625 21 18.2625V6C21 5.175 20.7062 4.46875 20.1187 3.88125C19.5312 3.29375 18.825 3 18 3C17.175 3 16.4688 3.29375 15.8813 3.88125C15.2938 4.46875 15 5.175 15 6V21C15 22.65 14.4125 24.0625 13.2375 25.2375C12.0625 26.4125 10.65 27 9 27ZM4.5 6C4.925 6 5.28125 5.85625 5.56875 5.56875C5.85625 5.28125 6 4.925 6 4.5C6 4.075 5.85625 3.71875 5.56875 3.43125C5.28125 3.14375 4.925 3 4.5 3C4.075 3 3.71875 3.14375 3.43125 3.43125C3.14375 3.71875 3 4.075 3 4.5C3 4.925 3.14375 5.28125 3.43125 5.56875C3.71875 5.85625 4.075 6 4.5 6ZM22.5 24C22.925 24 23.2812 23.8563 23.5688 23.5688C23.8563 23.2812 24 22.925 24 22.5C24 22.075 23.8563 21.7188 23.5688 21.4312C23.2812 21.1437 22.925 21 22.5 21C22.075 21 21.7188 21.1437 21.4312 21.4312C21.1437 21.7188 21 22.075 21 22.5C21 22.925 21.1437 23.2812 21.4312 23.5688C21.7188 23.8563 22.075 24 22.5 24Z" fill="#005E97"/>
                </svg>
                <div>
                  <div style={{ display: "flex", alignItems: "baseline", gap: 4 }}>
                    <span className="stat-number garamond">1,240</span>
                    <span className="stat-unit">km</span>
                  </div>
                  <p className="stat-label-lg">Kilometers Explored</p>
                </div>
              </div>

              {/* Cultural gems */}
              <div className="bento-card bento-card-blue">
                <svg width="30" height="32" viewBox="0 0 30 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M0 31.5V15H3V18H6L10.4625 3.1875V0H13.4625V3H16.5V0H19.5V3L24 18H27V15H30V31.5H16.5V24H13.5V31.5H0ZM10.05 15H19.95L19.05 12H10.95L10.05 15ZM11.85 9H18.15L17.25 6H12.75L11.85 9ZM3 28.5H10.5V21H19.5V28.5H27V21H21.75L20.85 18H9.15L8.25 21H3V28.5Z" fill="#005E97"/>
                </svg>
                <div>
                  <p className="stat-number-sm garamond">42</p>
                  <p className="stat-label">Cultural Gems Discovered</p>
                </div>
              </div>
            </div>
          </section>

          {/* ── Saved Itineraries ── */}
          <section style={{ display: "flex", flexDirection: "column", gap: 32 }}>
            <div className="section-header">
              <h2 className="section-title garamond">Saved Itineraries</h2>
              <button className="view-all-btn">
                View All
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12.175 9H0V7H12.175L6.575 1.4L8 0L16 8L8 16L6.575 14.6L12.175 9Z" fill="#005E97"/>
                </svg>
              </button>
            </div>

            <div className="itineraries-scroll">
              {itineraries.map((item) => (
                <div key={item.id} className="itinerary-card">
                  <img src={item.image} alt={item.title} />
                  <div className="itinerary-overlay" />
                  <div className="itinerary-info">
                    <p className="itinerary-duration">{item.duration}</p>
                    <h3 className="itinerary-title garamond">{item.title}</h3>
                    <div className="itinerary-tags">
                      {item.tags.map((tag) => (
                        <span key={tag} className="itinerary-tag">{tag}</span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* ── Intelligence Preferences ── */}
          <section className="preferences-panel">
            <div className="pref-header">
              <h2 className="section-title garamond">Intelligence Preferences</h2>
              <p className="pref-subtitle">
                Set your available travel duration. Algiers AI builds the optimal path that maximizes your cultural interest and exploration within your time budget.
              </p>
            </div>

            <div className="time-budget-container">
              <div className="time-budget-header">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#005E97" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
                <h4 className="time-budget-title">Duration Budget</h4>
              </div>
              <div className="time-budget-display garamond">
                {timeBudget} <span className="time-budget-unit">Hours</span>
              </div>
              <div className="slider-wrap" style={{ width: "100%" }}>
                <input
                  type="range"
                  min="2" max="24"
                  value={timeBudget}
                  onChange={(e) => setTimeBudget(Number(e.target.value))}
                  className="range-input"
                  style={{ "--pct": sliderPct }}
                />
                <div className="slider-labels">
                  <span>2 hours</span>
                  <span>12 hours</span>
                  <span>24 hours</span>
                </div>
                <p className="slider-desc" style={{ textAlign: "center", marginTop: "16px" }}>
                  Algiers AI will optimize your experience to prioritize the most interesting landmarks within a {timeBudget}-hour window.
                </p>
              </div>
            </div>
          </section>

        </main>
      </div>
    </>
  );
}