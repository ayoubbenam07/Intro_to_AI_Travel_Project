import React from "react";
import Papa from "papaparse";

/* ───────────────────── type-icon mapping ───────────────────── */
const ICON_PATHS = {
  Monument: `<path d="M3 22h18M6 18v-7M10 18v-7M14 18v-7M18 18v-7M12 2L3 7v4h18V7l-9-5z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  Nature: `<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 8a7 7 0 0 1-13.9 3.9M9 22v-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  "Historical Site": `<path d="M22 20v-9H2v9a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zM18 11V4h-2v3h-2V4h-2v3H8V4H6v3H4V4H2v7M12 22v-4a2 2 0 0 0-4 0v4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  Mosque: `<path d="M12 2a1 1 0 0 1 .7.3l.3.7v1c2.8.2 5 2.5 5 5v3h2a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1h2v-3c0-2.5 2.2-4.8 5-5V4a1 1 0 0 1 1-2zm-6 9v8h12v-8H6z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  Cathedral: `<path d="M10 20V14h4v6M14 2v4h-4V2M6 6h12M12 22V8M18 22H6M20 14H4M18 8l-6-6-6 6M18 12V8M6 12V8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  Museum: `<path d="M12 22C17.5 22 22 17.5 22 12S17.5 2 12 2 2 6.5 2 12s4.5 10 10 10z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="7.5" cy="10.5" r="1.5" fill="currentColor"/><circle cx="11.5" cy="7.5" r="1.5" fill="currentColor"/><circle cx="16.5" cy="9.5" r="1.5" fill="currentColor"/><circle cx="15.5" cy="14.5" r="1.5" fill="currentColor"/>`,
  "Cultural Center & Event Venue": `<path d="M12 22c5.5 0 10-4.5 10-10S17.5 2 12 2 2 6.5 2 12s4.5 10 10 10zM8 14h8M9 9h.01M15 9h.01M10 11.5a2 2 0 0 0 4 0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  Park: `<path d="M17 14A5 5 0 1 0 7 14c0 3 2.72 5.5 6 5.5V22h2v-2.5c3.28 0 6-2.5 6-5.5z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  "Public Square": `<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="10" r="3" fill="currentColor"/>`,
  Beach: `<path d="M23 12a11 11 0 0 0-22 0h22zM12 12v9a1 1 0 0 0 1 1h1M12 12a4 4 0 0 0 4-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  "Shopping/Mall": `<path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6zM3 6h18M16 10a4 4 0 0 1-8 0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  Hotel: `<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v3a2 2 0 0 0 4 0V8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`,
  Default: `<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`
};

const TYPE_COLORS = {
  Monument:                     "#e74c3c",
  Nature:                       "#27ae60",
  "Historical Site":            "#8e44ad",
  Mosque:                       "#2980b9",
  Cathedral:                    "#c0392b",
  Museum:                       "#e67e22",
  "Cultural Center & Event Venue": "#d35400",
  Park:                         "#2ecc71",
  "Public Square":              "#3498db",
  Beach:                        "#1abc9c",
  "Shopping/Mall":              "#9b59b6",
};

export function getTypeIconSvg(type) {
  return ICON_PATHS[type] || ICON_PATHS.Default;
}

export function getTypeIcon(type) {
  const path = ICON_PATHS[type] || ICON_PATHS.Default;
  return React.createElement("svg", {
    viewBox: "0 0 24 24",
    width: "20px",
    height: "20px",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    style: { display: "inline-block", verticalAlign: "middle" },
    dangerouslySetInnerHTML: { __html: path }
  });
}

export function getTypeColor(type) {
  return TYPE_COLORS[type] || "#7f8c8d";
}

/* ───────────────── CSV fetch + parse ───────────────── */

function fetchCSV(url) {
  return new Promise((resolve, reject) => {
    Papa.parse(url, {
      download: true,
      header: true,
      skipEmptyLines: true,
      complete: (results) => resolve(results.data),
      error: (err) => reject(err),
    });
  });
}

/**
 * Parse a landmarks row into a clean JS object.
 * The CSV columns are:
 * ID, Name, Description, Type, Rating, Latitude, Longitude, EstimatedTime (min), Hours, Images
 */
function parseLandmark(row) {
  let hours = null;
  try {
    const rawHours = (row["Hours"] || "").trim();
    if (rawHours && rawHours !== ".") {
      hours = JSON.parse(rawHours);
    }
  } catch {
    hours = null;
  }

  return {
    id:             parseInt(row["ID"], 10),
    name:           (row["Name"] || "").trim(),
    description:    (row["Description"] || "").trim(),
    type:           (row["Type"] || "").trim(),
    rating:         parseFloat(row["Rating"]) || 0,
    latitude:       parseFloat(row["Latitude"]),
    longitude:      parseFloat(row["Longitude"]),
    estimatedTime:  parseInt(row["EstimatedTime (min)"], 10) || 0,
    hours,
    images:         (row["Images"] || "").trim(),
    icon:           getTypeIcon((row["Type"] || "").trim()),
    color:          getTypeColor((row["Type"] || "").trim()),
  };
}

function parseHotel(row) {
  return normalizeHotelRecord({
    id: `hotel-${row["name"]}`,
    name: row["name"],
    latitude: row["latitude"],
    longitude: row["longitude"],
  });
}

/** Normalize API/CSV hotel records to a consistent shape */
export function normalizeHotelRecord(h) {
  const name = (h?.name || "").trim();
  const latitude = Number(h?.latitude ?? h?.lat);
  const longitude = Number(h?.longitude ?? h?.lon);
  return {
    id: h?.id ?? `hotel-${name}`,
    name,
    latitude,
    longitude,
    type: h?.type || "Hotel",
    icon: h?.icon || getTypeIcon("Hotel"),
    color: h?.color || "#f39c12",
  };
}

/** Match backend/frontend hotel name variants (e.g. "Hôtel RALF" vs "RALF Hotel") */
export function normalizeHotelName(name) {
  if (!name) return "";
  return name   
}

export function findHotelByName(hotels, nameOrHotel) {
  if (!hotels?.length && !(nameOrHotel?.latitude != null)) return null;

  if (nameOrHotel && typeof nameOrHotel === "object") {
    const lat = Number(nameOrHotel.latitude ?? nameOrHotel.lat);
    const lon = Number(nameOrHotel.longitude ?? nameOrHotel.lon);
    if (!Number.isNaN(lat) && !Number.isNaN(lon) && hotels?.length) {
      const byCoords = hotels.find(
        (h) =>
          Math.abs(h.latitude - lat) < 0.0002 &&
          Math.abs(h.longitude - lon) < 0.0002,
      );
      if (byCoords) return byCoords;
    }
    if (nameOrHotel.name && hotels?.length) {
      const byName = findHotelByName(hotels, nameOrHotel.name);
      if (byName) return byName;
    }
    if (!Number.isNaN(lat) && !Number.isNaN(lon)) {
      return normalizeHotelRecord(nameOrHotel);
    }
  }

  const name = typeof nameOrHotel === "string" ? nameOrHotel.trim() : null;
  if (!name || !hotels?.length) return null;

  const exact = hotels.find((h) => h.name === name);
  if (exact) return exact;

  const target = normalizeHotelName(name);
  if (!target) return null;

  return (
    hotels.find((h) => {
      const n = normalizeHotelName(h.name);
      return n === target || n.includes(target) || target.includes(n);
    }) ?? null
  );
}

export async function loadLandmarks() {
  try {
    const rows = await fetchCSV("/data/Algiers_Landmarks.csv");
    return rows.map(parseLandmark).filter((l) => !Number.isNaN(l.latitude) && !Number.isNaN(l.longitude) && l.id);
  } catch (err) {
    console.error("Failed to load landmarks CSV:", err);
    return [];
  }
}

let cachedHotels = null;
const HOTEL_REQUEST_TIMEOUT_MS = 10000;
const DEFAULT_API_BASES = [
  import.meta.env.VITE_API_BASE_URL,
  "http://127.0.0.1:8000",
  "http://localhost:8000",
  "https://intro-to-ai-travel-project-2.onrender.com",
].filter(Boolean);

function getHotelsApiCandidates() {
  return [...new Set(DEFAULT_API_BASES)].map((base) => `${base.replace(/\/$/, "")}/api/hotels`);
}

export async function loadHotels() {
  // 2. Check cache
  if (cachedHotels) {
    return cachedHotels;
  }

  for (const endpoint of getHotelsApiCandidates()) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), HOTEL_REQUEST_TIMEOUT_MS);

    try {
      const res = await fetch(endpoint, { signal: controller.signal });
      clearTimeout(timeoutId);
      if (!res.ok) {
        continue;
      }

      const raw = await res.json();
      const hotelRows = Array.isArray(raw) ? raw : Array.isArray(raw?.hotels) ? raw.hotels : [];
      if (hotelRows.length > 0) {
        cachedHotels = hotelRows
          .map(normalizeHotelRecord)
          .filter((h) => !Number.isNaN(h.latitude) && !Number.isNaN(h.longitude));
        return cachedHotels;
      }
    } catch (err) {
      clearTimeout(timeoutId);
      console.warn(`Failed to load hotels from ${endpoint}:`, err);
    }
  }

  try {
    const rows = await fetchCSV("/data/Algiers_hotels.csv");
    cachedHotels = rows.map(parseHotel).filter((h) => !Number.isNaN(h.latitude) && !Number.isNaN(h.longitude));
    return cachedHotels;
  } catch (csvErr) {
    console.error("Failed to load local fallback hotels CSV:", csvErr);
    return [];
  }
}

