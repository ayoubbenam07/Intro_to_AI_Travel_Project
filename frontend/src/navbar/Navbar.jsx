import { useState } from "react";


const styles = `
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  /* ── Outer wrapper ── */
  .navbar-wrap {
    width: 92%;
    max-width: 980px;
    background: rgba(255, 255, 255, 0.74);
    backdrop-filter: blur(24px) saturate(1.7);
    -webkit-backdrop-filter: blur(24px) saturate(1.7);
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.88);
    box-shadow:
      0 8px 32px rgba(0, 35, 102, 0.16),
      0 1.5px 0 rgba(255,255,255,0.92) inset;
    padding: 0 10px 0 20px;
    display: flex;
    align-items: center;
    height: 56px;
    gap: 0;
    position: fixed;
    top: 24px;
    left: 0;
    right: 0;
    margin: 0 auto;
    z-index: 1000;
    transition: box-shadow 0.3s;
    animation: navbar-in 0.55s cubic-bezier(.22,1,.36,1) both;
  }
  .navbar-wrap:hover {
    box-shadow:
      0 12px 40px rgba(0, 35, 102, 0.22),
      0 1.5px 0 rgba(255,255,255,0.92) inset;
  }

  /* ── Brand ── */
  .brand {
    font-family: var(--font-headline);
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--color-tertiary);
    letter-spacing: -0.01em;
    white-space: nowrap;
    margin-right: 28px;
    cursor: pointer;
    user-select: none;
    flex-shrink: 0;
    transition: color 0.2s;
  }
  .brand:hover { color: var(--color-primary); }

  /* ── Divider ── */
  .divider {
    width: 1px;
    height: 26px;
    background: linear-gradient(to bottom, transparent, rgba(0, 35, 102, 0.20), transparent);
    flex-shrink: 0;
    margin-right: 20px;
  }

  /* ── Nav links ── */
  .nav-links {
    display: flex;
    align-items: center;
    gap: 2px;
    flex: 1;
  }

  .nav-link {
    position: relative;
    font-family: var(--font-body);
    font-size: var(--text-sm);
    font-weight: 400;
    color: var(--color-tertiary);
    opacity: 0.7;
    background: none;
    border: none;
    cursor: pointer;
    padding: 6px 14px;
    border-radius: 999px;
    letter-spacing: 0.01em;
    transition: color 0.2s, background 0.2s, opacity 0.2s;
    white-space: nowrap;
    line-height: 1;
    outline: none;
  }
  .nav-link:hover {
    color: var(--color-tertiary);
    opacity: 1;
    background: rgba(0, 35, 102, 0.10);
  }

  /* Active tab */
  .nav-link.active {
    color: var(--color-primary);
    opacity: 1;
    font-weight: 500;
  }
  .nav-link.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 2px;
    background: var(--color-primary);
    border-radius: 2px;
    animation: underline-in 0.25s cubic-bezier(.4,0,.2,1) both;
  }
  @keyframes underline-in {
    from { width: 0; opacity: 0; }
    to   { width: 60%; opacity: 1; }
  }

  /* Hover underline for non-active links */
  .nav-link:not(.active)::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 2px;
    background: var(--color-primary);
    border-radius: 2px;
    transition: width 0.2s ease;
    opacity: 0.45;
  }
  .nav-link:not(.active):hover::after { width: 40%; }

  /* ── Right side ── */
  .nav-right {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-left: auto;
    flex-shrink: 0;
  }

  /* AI Assistant button — Primary fill */
  .btn-ai {
    display: flex;
    align-items: center;
    gap: 7px;
    background: var(--color-primary);
    color: var(--color-neutral);
    font-family: var(--font-body);
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    border: none;
    border-radius: 999px;
    padding: 8px 17px 8px 13px;
    cursor: pointer;
    white-space: nowrap;
    box-shadow: 0 2px 14px rgba(0, 119, 190, 0.38);
    transition: background 0.2s, box-shadow 0.2s, transform 0.15s;
    outline: none;
    position: relative;
    overflow: hidden;
  }
  /* Subtle cyan shimmer from secondary token */
  .btn-ai::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(125, 249, 255, 0.22) 0%, transparent 55%);
    border-radius: 999px;
    pointer-events: none;
  }
  .btn-ai:hover {
    background: var(--color-primary-hover);
    box-shadow: 0 4px 22px rgba(0, 119, 190, 0.48);
    transform: translateY(-1px);
  }
  .btn-ai:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(0, 119, 190, 0.3);
  }

  .btn-ai-icon {
    width: 15px;
    height: 15px;
    flex-shrink: 0;
    opacity: 0.92;
  }

  /* Avatar / user icon — Tertiary tint */
  .avatar-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(0, 35, 102, 0.10);
    border: 1.5px solid rgba(0, 35, 102, 0.20);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s, transform 0.15s;
    outline: none;
    color: var(--color-tertiary);
    flex-shrink: 0;
  }
  .avatar-btn:hover {
    background: rgba(0, 35, 102, 0.20);
    border-color: rgba(0, 35, 102, 0.35);
    transform: scale(1.06);
  }

  /* ── Sign in button ── */
  .btn-signin {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    color: var(--color-primary);
    border: 1.5px solid var(--color-primary);
    border-radius: 999px;
    font-family: var(--font-body);
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    padding: 8px 18px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
    outline: none;
    line-height: 1;
    text-decoration: none;
  }
  .btn-signin:hover {
    background: var(--color-primary);
    color: var(--color-neutral);
    box-shadow: 0 4px 14px rgba(0, 119, 190, 0.25);
  }

  /* ── Entry animation ── */
  @keyframes navbar-in {
    from { opacity: 0; transform: translateY(-14px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }

  /* ── Responsive ── */
  @media (max-width: 680px) {
    .navbar-wrap { padding: 0 8px 0 14px; height: 50px; margin: 12px auto 0 auto; }
    .brand { font-size: 1.05rem; margin-right: 14px; }
    .divider { display: none; }
    .nav-link { padding: 5px 9px; font-size: 0.8rem; }
    .btn-ai { padding: 7px 13px 7px 10px; font-size: 0.78rem; }
    .btn-signin { padding: 6px 12px; font-size: 0.76rem; }
  }
  @media (max-width: 480px) {
    .nav-links .nav-link:nth-child(n+3) { display: none; }
    .btn-ai-text { display: none; }
    .btn-ai { padding: 8px; }
    .nav-right { gap: 8px; }
    .nav-links { gap: 4px; }
    .brand { margin-right: 8px; font-size: 0.95rem; }
  }
`;

// ─── SVG Icons ────────────────────────────────────────────────────────────────

const SparkleIcon = () => (
  <svg className="btn-ai-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M12 2L13.5 8.5L20 10L13.5 11.5L12 18L10.5 11.5L4 10L10.5 8.5L12 2Z"
      fill="white"
      fillOpacity="0.95"
    />
    <path
      d="M19 16L19.75 18.25L22 19L19.75 19.75L19 22L18.25 19.75L16 19L18.25 18.25L19 16Z"
      fill="white"
      fillOpacity="0.7"
    />
  </svg>
);

const UserIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="8" r="4" />
    <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
  </svg>
);

// ─── Data ─────────────────────────────────────────────────────────────────────

const NAV_ITEMS = [
  { label: "Home", path: "/" },
  { label: "Itinerary", path: "/itinerary" },
  { label: "Plan Journey", path: "/plan" }
];

// ─── Component ────────────────────────────────────────────────────────────────

import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();
  const activePath = location.pathname;
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

  return (
    <>
      <style>{styles}</style>

      <nav className="navbar-wrap" role="navigation" aria-label="Main navigation">

        {/* Brand */}
        <Link to="/" className="brand" role="link" tabIndex={0} style={{ textDecoration: 'none' }}>
          Algiers AI
        </Link>

        {/* Vertical divider */}
        <div className="divider" aria-hidden="true" />

        {/* Nav Links */}
        <div className="nav-links" role="menubar">
          {NAV_ITEMS.map((item) => (
            <Link
              to={item.path}
              key={item.label}
              className={`nav-link${activePath === item.path ? " active" : ""}`}
              role="menuitem"
              aria-current={activePath === item.path ? "page" : undefined}
              style={{ textDecoration: 'none' }}
            >
              {item.label}
            </Link>
          ))}
        </div>

        {/* Right controls */}
        <div className="nav-right">
          <Link to="/plan" className="btn-ai" aria-label="Open AI Planner" style={{ textDecoration: 'none' }}>
            <SparkleIcon />
            <span className="btn-ai-text">AI Planner</span>
          </Link>
          {isLoggedIn ? (
            <Link to="/profile" className="avatar-btn" aria-label="User profile" style={{ textDecoration: 'none' }}>
              <UserIcon />
            </Link>
          ) : (
            <Link to="/login" className="btn-signin" style={{ textDecoration: 'none' }}>
              Sign In
            </Link>
          )}
        </div>

      </nav>
    </>
  );
}