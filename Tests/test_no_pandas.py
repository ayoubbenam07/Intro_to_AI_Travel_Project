import os
import json
import csv

def get_landmarks_no_pandas(csv_path):
    landmarks = []
    # Simplified parsing for testing
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Reconstruct Landmark-like data
            # Note: core.Node_Classes might still be okay if it doesn't import pandas
            landmarks.append(row)
    return landmarks

if __name__ == "__main__":
    path = r"e:\School project\Intro_to_AI_Travel_Project\dataset\landmarks\Algiers_Landmarks.csv"
    if os.path.exists(path):
        data = get_landmarks_no_pandas(path)
        print(f"Loaded {len(data)} landmarks without pandas")
    else:
        print("Path not found")
