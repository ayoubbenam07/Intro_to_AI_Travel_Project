import pandas as pd
from geopy.geocoders import Nominatim
import time

# 1. Load the CSV we generated earlier
input_file = "dataset.csv"
output_file = "final_dataset.csv"

try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Error: Could not find {input_file}. Make sure it is in the same folder.")
    exit()

# 2. Initialize the geocoder
# Nominatim requires a unique user_agent name for your app
geolocator = Nominatim(user_agent="algiers_touristic_guide_builder")

# 3. Define the function to fetch coordinates
def get_coordinates(landmark_name):
    # Appending the city and country vastly improves accuracy
    query = f"{landmark_name}, Algiers, Algeria"
    try:
        # Timeout set to 10 seconds to handle slow network responses
        location = geolocator.geocode(query, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"  [!] Error fetching {landmark_name}: {e}")
        return None, None

print(f"Starting geocoding for {len(df)} landmarks...")
print("Please wait. This will take about 1-2 minutes to respect server rate limits.\n")

lats = []
lons = []

# 4. Loop through the dataset
for index, row in df.iterrows():
    name = row['Name']
    print(f"[{index + 1}/{len(df)}] Locating: {name}...")
    
    lat, lon = get_coordinates(name)
    lats.append(lat)
    lons.append(lon)
    
    # CRITICAL: Sleep for 1.5 seconds to respect Nominatim's free usage policy
    time.sleep(1.5)

# 5. Add the new data to the DataFrame and save it
df['Latitude'] = lats
df['Longitude'] = lons

df.to_csv(output_file, index=False)
print(f"\nSuccess! Your new dataset is saved as: {output_file}")