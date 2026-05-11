import pandas as pd
import numpy as np
import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

landmarks = pd.read_csv(os.path.join(BASE_DIR, "../dataset/landmarks/Algiers_Landmarks.csv"))
hotels    = pd.read_csv(os.path.join(BASE_DIR, "../dataset/hotels/Algiers_hotels.csv"))

names = list(landmarks["Name"]) + list(hotels["name"])

all_coords = (
    [(row["Longitude"], row["Latitude"]) for _, row in landmarks.iterrows()] +
    [(row["longitude"], row["latitude"]) for _, row in hotels.iterrows()]
)

OSRM_BASE = "http://router.project-osrm.org/table/v1/driving"
BATCH     = 100

n = len(all_coords)
time_matrix = np.zeros((n, n), dtype=float)

for i in range(0, n, BATCH):
    for j in range(0, n, BATCH):
        src_slice = all_coords[i:i+BATCH]
        dst_slice = all_coords[j:j+BATCH]

        combined = src_slice + dst_slice
        coords_str = ";".join(f"{lon},{lat}" for lon, lat in combined)

        sources      = ";".join(str(k) for k in range(len(src_slice)))
        destinations = ";".join(str(k + len(src_slice)) for k in range(len(dst_slice)))

        r = requests.get(
            f"{OSRM_BASE}/{coords_str}",
            params={"annotations": "duration", "sources": sources, "destinations": destinations},
            timeout=120
        )
        r.raise_for_status()
        block = np.array(r.json()["durations"], dtype=float) / 60  # seconds → minutes
        time_matrix[i:i+len(src_slice), j:j+len(dst_slice)] = block

np.save(os.path.join(BASE_DIR, "time_matrix.npy"), time_matrix)

df = pd.DataFrame(time_matrix.round(1), index=names, columns=names)
df.to_csv(os.path.join(BASE_DIR, "time_matrix_named.csv"))

print(f"Done. Matrix shape: {time_matrix.shape}")

# Convert time_matrix_named.csv → time_matrix.json
df = pd.read_csv(os.path.join(BASE_DIR, "time_matrix_named.csv"), index_col=0)

time_dict = {}
for start in df.index:
    time_dict[start] = {}
    for end in df.columns:
        time_dict[start][end] = round(float(df.loc[start, end]), 1)

with open(os.path.join(BASE_DIR, "time_matrix.json"), "w", encoding="utf-8") as f:
    json.dump(time_dict, f, ensure_ascii=False, indent=2)

print("Done. Saved to time_matrix.json")