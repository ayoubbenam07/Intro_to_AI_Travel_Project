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
    z-index: 2;
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
    font-family: var(--font-headline);
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

  const rawName = user?.full_name || (localStorage.getItem("user_email") || localStorage.getItem("userEmail") || "Meghabber Mohammed Al Ghazali").split("@")[0];
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
                  <h1 className="hero-name garamond">Meghabber mohammed Al Ghazali</h1>
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
                    <span className="stat-number garamond">{totalKm.toFixed(1)}</span>
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
                  <p className="stat-number-sm garamond">{uniqueGems.size}</p>
                  <p className="stat-label">Cultural Gems Discovered</p>
                </div>
              </div>
            </div>
          </section>

          {/* ── Journey History ── */}
          <section style={{ display: "flex", flexDirection: "column", gap: 32 }}>
            <div className="section-header">
              <h2 className="section-title garamond">Journey History</h2>
            </div>

            <div className="itineraries-scroll">
              {dbItineraries.length === 0 ? (
                <div style={{
                  gridColumn: "span 3",
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
                dbItineraries.map((item, idx) => (
                  <div key={item.itinerary_id} className="itinerary-card" onClick={() => handleCardClick(item)}>
                    <button 
                      className="delete-itinerary-btn" 
                      onClick={(e) => handleDelete(item.itinerary_id, e)}
                      title="Delete Itinerary"
                    >
                      🗑️
                    </button>
                    <img src={IMAGES[idx % IMAGES.length]} alt={item.name} />
                    <div className="itinerary-overlay" />
                    <div className="itinerary-info">
                      <p className="itinerary-duration">
                        {item.time_budget_hours ? `${item.time_budget_hours} Hours` : "24h"} • {(item.algorithm || "AI").toUpperCase()}
                      </p>
                      <h3 className="itinerary-title garamond">{item.name}</h3>
                      <div className="itinerary-tags">
                        <span className="itinerary-tag">{item.itinerary_type.replace('_', ' ').toUpperCase()}</span>
                        <span className="itinerary-tag">{item.travel_day}</span>
                      </div>
                    </div>
                  </div>
                ))
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