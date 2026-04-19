from outscraper import ApiClient
import pandas as pd
import datetime

API_KEY = "PUT_YOUR_KEY_HERE"
client = ApiClient(api_key=API_KEY)

# Algiers center: 36.7538, 3.0588 - 25km radius covers the whole city
results = client.google_maps_search(
    [
        "famous landmarks Algiers",
        "monument Alger",
        "tourist attraction Alger",
        "museum Alger",
        "mosque Alger"
    ],
    limit=40, # keep it small to stay free
    language="en", # English makes hours easier to parse
    region="DZ",
    coordinates="36.7538,3.0588,25000",
)

# --- Parse the data you need ---
today = datetime.datetime.now().strftime("%A") # Monday, Tuesday...

rows = []
for place in results:
    name = place.get("name")
    rating = place.get("rating")
    lat = place.get("latitude")
    lng = place.get("longitude")
    address = place.get("full_address")

    # opening hours - Outscraper returns a dict
    working = place.get("working_hours", {})
    hours_raw = " | ".join([f"{k}: {v}" for k, v in working.items()]) if working else ""

    today_hours = working.get(today, "")
    open_time, close_time = None, None
    if today_hours and "Closed" not in today_hours:
        # format is "9 AM – 5 PM"
        parts = today_hours.replace("–", "-").split("-")
        if len(parts) == 2:
            open_time = parts[0].strip()
            close_time = parts[1].strip()

    description = place.get("about", {}).get("summary") or place.get("description", "")

    # first photo
    photos = place.get("photos", [])
    image_url = photos[0].get("photo_url") if photos else ""

    rows.append({
        "name": name,
        "rating": rating,
        "latitude": lat,
        "longitude": lng,
        "address": address,
        "opening_hour_today": open_time,
        "closing_hour_today": close_time,
        "opening_hours_full": hours_raw,
        "description": description,
        "image_url": image_url,
        "google_maps_url": place.get("place_link")
    })

df = pd.DataFrame(rows)
# remove duplicates by name
df = df.drop_duplicates("name")

df.to_csv("algiers_landmarks.csv", index=False, encoding="utf-8")
print(f"Saved {len(df)} landmarks to algiers_landmarks.csv")
print(df[["name", "rating", "opening_hour_today", "closing_hour_today"]].head(10))