import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

const IMAGES = [
  "https://images.unsplash.com/photo-1566847438233-97be722885c5?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=800&q=80",
  "https://images.unsplash.com/photo-1582298538104-fc2c0a5a0028?auto=format&fit=crop&w=800&q=80"
];

const styles = `
  .profile-root {
    min-height: 100vh;
    background: #F9F9F9;
    font-family: var(--font-body);
    overflow-x: hidden;
  }

  .garamond { font-family: var(--font-headline); }

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
    background: linear-gradient(135deg, var(--color-tertiary) 0%, var(--color-primary) 50%, var(--color-secondary) 100%);
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
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-tertiary) 100%);
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
    font-family: var(--font-headline);
    font-size: 28px;
    font-weight: 500;
    color: var(--color-neutral-1000);
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
    font-family: var(--font-headline);
    font-size: 28px;
    font-weight: 500;
    color: var(--color-neutral-1000);
    line-height: 1.2;
  }
  @media (min-width: 640px) { .section-title { font-size: 36px; } }
  @media (min-width: 1024px) { .section-title { font-size: 48px; } }

  .ai-badge {
    font-size: 11px;
    font-weight: 700;
    color: var(--color-primary);
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
    font-family: var(--font-headline);
    font-size: 48px;
    font-weight: 400;
    color: var(--color-neutral-1000);
    line-height: 1;
  }
  @media (min-width: 1024px) { .stat-number { font-size: 60px; } }

  .stat-number-sm {
    font-family: var(--font-headline);
    font-size: 36px;
    font-weight: 400;
    color: var(--color-neutral-1000);
    line-height: 1.1;
  }

  .stat-unit {
    font-size: 18px;
    color: var(--color-neutral-500);
  }

  .stat-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--color-neutral-800);
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-top: 8px;
  }

  .stat-label-lg {
    font-size: 16px;
    font-weight: 600;
    color: var(--color-neutral-800);
    letter-spacing: 1px;
    margin-top: 8px;
  }
  @media (min-width: 1024px) { .stat-label-lg { font-size: 20px; } }

  /* ── Itineraries Grid ── */
  .itineraries-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
    width: 100%;
  }

  .itinerary-card {
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 24px;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(0, 94, 151, 0.15);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
  }
  .itinerary-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 20px -3px rgba(0,0,0,0.1);
    background: rgba(255, 255, 255, 0.9);
  }
  .itinerary-card:hover .card-arrow-btn {
    transform: translateX(4px);
  }

  .itinerary-info {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .itinerary-duration {
    font-size: 12px;
    font-weight: 700;
    color: var(--color-primary);
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  .itinerary-title {
    font-family: var(--font-headline);
    font-size: 20px;
    font-weight: 600;
    color: var(--color-tertiary);
    line-height: 1.3;
  }

  .itinerary-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: auto;
    padding-top: 12px;
  }

  .itinerary-tag {
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(0, 94, 151, 0.08);
    font-size: 12px;
    font-weight: 600;
    color: var(--color-primary);
  }
  
  .profile-loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 0;
    gap: 20px;
    grid-column: 1 / -1;
  }
  .profile-loader__spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(0, 94, 151, 0.1);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: profile-spin 1s linear infinite;
  }
  @keyframes profile-spin {
    to { transform: rotate(360deg); }
  }

  .view-all-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--color-primary);
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
    color: var(--color-neutral-800);
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
    color: var(--color-primary);
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
    border-color: var(--color-primary);
    background: rgba(0,94,151,0.08);
    box-shadow: 0 4px 14px rgba(0,105,109,0.08);
  }

  .budget-label {
    font-size: 15px;
    color: var(--color-neutral-800);
  }
  .budget-label.active {
    font-weight: 700;
    color: var(--color-primary);
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
    background: var(--color-primary);
    border-color: var(--color-primary);
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
    background: linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) var(--pct, 50%), #D1D8E2 var(--pct, 50%), #D1D8E2 100%);
    outline: none;
    cursor: pointer;
  }
  .range-input::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px; height: 20px;
    border-radius: 50%;
    background: var(--color-primary);
    box-shadow: 0 2px 8px rgba(0,94,151,0.30);
    cursor: pointer;
    transition: transform 0.15s;
  }
  .range-input::-webkit-slider-thumb:hover { transform: scale(1.2); }
  .range-input::-moz-range-thumb {
    width: 20px; height: 20px;
    border-radius: 50%;
    background: var(--color-primary);
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
    color: var(--color-neutral-500);
    transition: color 0.2s;
  }
  .slider-label.active {
    color: var(--color-primary);
    font-weight: 700;
  }

  .slider-desc {
    font-size: 13px;
    color: var(--color-neutral-800);
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
    color: var(--color-neutral-800);
    background: transparent;
    cursor: pointer;
    transition: all 0.2s;
  }
  .chip.active {
    border-color: var(--color-primary);
    background: rgba(0,94,151,0.06);
    color: var(--color-primary);
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
    color: var(--color-primary);
    letter-spacing: 1px;
  }

  .time-budget-display {
    font-size: 64px;
    font-weight: 700;
    color: var(--color-neutral-1000);
    line-height: 1;
    display: flex;
    align-items: baseline;
    gap: 8px;
  }

  .time-budget-unit {
    font-size: 24px;
    color: var(--color-neutral-500);
    font-weight: 400;
  }

  .delete-itinerary-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 5;
    background: rgba(192, 57, 43, 0.9);
    border: none;
    color: white;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.2s, transform 0.2s;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  }
  .delete-itinerary-btn:hover {
    background: #c0392b;
    transform: scale(1.1);
  }
`;

export default function Profile() {

  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [dbItineraries, setDbItineraries] = useState([]);
  const [timeBudget, setTimeBudget] = useState(12);
  const [loading, setLoading] = useState(true);


  const sliderPct = `${((timeBudget - 2) / 22) * 100}%`;
  const userEmail = user?.email || localStorage.getItem("user_email") || localStorage.getItem("userEmail") || "guest@algiers.ai";

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        // Fetch real user info
        const userRes = await fetch("http://localhost:8000/api/me", {
          headers: { "Authorization": `Bearer ${token}` }
        });
        if (userRes.ok) {
          const userData = await userRes.json();
          setUser(userData);
        }

        // Fetch real itineraries
        const itinerariesRes = await fetch("http://localhost:8000/api/itineraries", {
          headers: { "Authorization": `Bearer ${token}` }
        });
        if (itinerariesRes.ok) {
          const itinerariesData = await itinerariesRes.json();
          setDbItineraries(itinerariesData);
        }
      } catch (err) {
        console.error("Error loading user profile:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_email");
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("userEmail");
    window.location.href = "/";
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this itinerary?")) return;
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(`http://localhost:8000/api/itineraries/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        setDbItineraries(prev => prev.filter(it => it.itinerary_id !== id));
      } else {
        alert("Failed to delete itinerary.");
      }
    } catch (err) {
      console.error(err);
      alert("Error deleting itinerary.");
    }
  };

  const handleCardClick = (itinerary) => {
    // Navigate to /itinerary passing the itinerary_id so Itinerary.jsx can fetch the path
    navigate("/itinerary", { 
      state: { 
        itineraryId: itinerary.itinerary_id,
        metadata: {
          name: itinerary.name,
          algorithm: itinerary.algorithm,
          evaluation_score: itinerary.evaluation_score,
          time_budget_hours: itinerary.time_budget_hours,
          travel_day: itinerary.travel_day
        }
      } 
    });
  };

  // Calculations for dynamic digital footprint
  const totalKm = dbItineraries.reduce((sum, itinerary) => {
    let dist = 0;
    const path = itinerary.path || [];
    for (let i = 0; i < path.length - 1; i++) {
      const p1 = path[i];
      const p2 = path[i + 1];
      if (p1.lat && p1.lon && p2.lat && p2.lon) {
        dist += calculateDistance(p1.lat, p1.lon, p2.lat, p2.lon);
      }
    }
    return sum + dist;
  }, 0);

  const uniqueGems = new Set();
  dbItineraries.forEach(itinerary => {
    const path = itinerary.path || [];
    path.forEach(landmark => {
      if (landmark.name) {
        uniqueGems.add(landmark.name);
      }
    });
  });

  const rawName = user?.full_name || (localStorage.getItem("user_email") || localStorage.getItem("userEmail") || "Traveler").split("@")[0];
  const displayName = rawName.split(/[\s._-]+/).map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");
  const userInitials = displayName.split(" ").map(n => n[0] || "").join("").substring(0, 2).toUpperCase() || "ME";

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
                  <span>{userInitials}</span>
                </div>

                <div className="hero-name-block" style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                  <h1 className="hero-name garamond">{displayName}</h1>
                  <span style={{ color: "rgba(0, 35, 102, 0.65)", fontFamily: "var(--font-body)", fontSize: "14.5px", fontWeight: 500 }}>{userEmail}</span>


                  <button 
                    onClick={handleLogout}
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
                      marginTop: 4,
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



          {/* ── Journey History ── */}
          <section style={{ display: "flex", flexDirection: "column", gap: 32 }}>
            <div className="section-header">
              <h2 className="section-title garamond">Journey History</h2>
            </div>

            <div className="itineraries-grid">
              {loading ? (
                <div className="profile-loader">
                  <div className="profile-loader__spinner" />
                  <p style={{ color: "var(--color-neutral-600)", fontWeight: 500 }}>Loading your journeys...</p>
                </div>
              ) : dbItineraries.length === 0 ? (
                <div style={{
                  gridColumn: "1 / -1",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  padding: "48px 24px",
                  borderRadius: "32px",
                  background: "rgba(255,255,255,0.40)",
                  border: "1px solid rgba(0,94,151,0.10)",
                  textAlign: "center",
                  gap: "16px",
                  width: "100%"
                }}>
                  <p className="garamond" style={{ fontSize: "24px", color: "var(--color-neutral-800)", margin: 0 }}>No journeys yet</p>
                  <p style={{ fontSize: "14px", color: "var(--color-neutral-500)", margin: 0, maxWidth: "400px" }}>
                    Your travel history in Algiers will appear here. Start planning to see your past itineraries!
                  </p>
                  <a href="/plan" style={{
                    textDecoration: "none",
                    padding: "12px 28px",
                    borderRadius: "999px",
                    background: "var(--color-primary)",
                    color: "white",
                    fontWeight: 600,
                    fontSize: "14px",
                    marginTop: "8px"
                  }}>
                    Plan a Journey
                  </a>
                </div>
              ) : (
                dbItineraries.map((item, idx) => {
                  const numLandmarks = (item.path || []).length;
                  const algoName = (item.algorithm || "AI").toUpperCase();
                  const hotelName = item.hotel_name || item.hotel || item.name?.split(" - ")[0] || "Algiers";
                  
                  return (
                    <div key={item.itinerary_id} className="itinerary-card" onClick={() => handleCardClick(item)}>
                      <div className="itinerary-info" style={{ flex: 1 }}>
                        <p className="itinerary-duration">
                          {numLandmarks} Landmarks • {algoName}
                        </p>
                        <h3 className="itinerary-title garamond">Start from {hotelName}</h3>
                        <div className="itinerary-tags">
                          <span className="itinerary-tag">{item.time_budget_hours ? `${item.time_budget_hours} Hours` : "24h"}</span>
                          <span className="itinerary-tag">{item.travel_day}</span>
                        </div>
                      </div>
                      
                      <div style={{
                        position: "absolute",
                        bottom: "24px",
                        right: "24px",
                        width: "40px",
                        height: "40px",
                        borderRadius: "50%",
                        background: "var(--color-primary)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "white",
                        boxShadow: "0 4px 12px rgba(0, 94, 151, 0.2)",
                        transition: "transform 0.2s"
                      }} className="card-arrow-btn">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginLeft: "2px" }}>
                          <polyline points="9 18 15 12 9 6" />
                        </svg>
                      </div>
                    </div>
                  );
                })
              )}
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
                  onChange={(e) => {
                    const val = Number(e.target.value);
                    setTimeBudget(val);
                    localStorage.setItem("selectedBudget", val.toString());
                  }}
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