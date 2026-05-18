import Papa from "papaparse";

/* ───────────────────── type-icon mapping ───────────────────── */
const TYPE_ICONS = {
  Monument:                     "🏛️",
  Nature:                       "🌿",
  "Historical Site":            "🏰",
  Mosque:                       "🕌",
  Cathedral:                    "⛪",
  Museum:                       "🎨",
  "Cultural Center & Event Venue": "🎭",
  Park:                         "🌳",
  "Public Square":              "📍",
  Beach:                        "🏖️",
  "Shopping/Mall":              "🛍️",
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

export function getTypeIcon(type) {
  return TYPE_ICONS[type] || "📌";
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
  return {
    id:             parseInt(row["ID"], 10),
    name:           (row["Name"] || "").trim(),
    description:    (row["Description"] || "").trim(),
    type:           (row["Type"] || "").trim(),
    rating:         parseFloat(row["Rating"]) || 0,
    latitude:       parseFloat(row["Latitude"]),
    longitude:      parseFloat(row["Longitude"]),
    estimatedTime:  parseInt(row["EstimatedTime (min)"], 10) || 0,
    icon:           getTypeIcon((row["Type"] || "").trim()),
    color:          getTypeColor((row["Type"] || "").trim()),
  };
}

function parseHotel(row) {
  return {
    id:        `hotel-${row["name"]}`,
    name:      (row["name"] || "").trim(),
    latitude:  parseFloat(row["latitude"]),
    longitude: parseFloat(row["longitude"]),
    type:      "Hotel",
    icon:      "🏨",
    color:     "#f39c12",
  };
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

export async function loadHotels() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 1500);

  try {
    const res = await fetch("http://localhost:8000/api/hotels", {
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    clearTimeout(timeoutId);
    console.error("Failed to load hotels from backend, falling back to local csv:", err);
  }

  try {
    const rows = await fetchCSV("/data/Algiers_hotels.csv");
    return rows.map(parseHotel).filter((h) => !Number.isNaN(h.latitude) && !Number.isNaN(h.longitude));
  } catch (csvErr) {
    console.error("Failed to load local fallback hotels CSV:", csvErr);
    return [];
  }
}

