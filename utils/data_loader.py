import pandas as pd
from pathlib import Path
from typing import Dict, List
from core.Node_Classes import Landmark, Hotel
import json


# .resolve() guarantees a full absolute path
_BASE_DIR = Path(__file__).resolve().parent.parent

# Path to CSV files 
LANDMARKS_PATH = _BASE_DIR / "dataset" / "landmarks" / "Algiers_Landmarks.csv"
HOTELS_PATH = _BASE_DIR / "dataset" / "hotels" / "Algiers_hotels.csv"
TIME_MATRIX_PATH = _BASE_DIR / "utils" / "time_matrix.json" 

def get_landmarks(landmarks_path=LANDMARKS_PATH):
    """
    Reads a CSV file containing landmark data, sets the first column as the index,
    and returns the data as a dictionary of dictionaries.

    Args:
        landmarks_path (str): Path to the landmarks CSV file.

    Returns:
        dict: Dictionary where each key is the value from the first column (index),
              and each value is another dictionary of column name -> value for that row.
    """
    df = pd.read_csv(landmarks_path)
    df['Hours'] = df['Hours'].apply(lambda x: json.loads(x.replace("'", '"')))  # Convert string to dict
    landmarks = []
    for idx, row in df.iterrows():
        landmark = Landmark(
            id=row['ID'],
            name=row['Name'],
            lon=row['Longitude'],
            lat=row['Latitude'],
            landmark_type=row['Type'],
            opening_hours=row['Hours'],
            visit_duration=row['EstimatedTime (min)'],
            interest_score=row['Rating']
        )
        landmarks.append(landmark)
    return landmarks

def get_hotels(hotels_path=HOTELS_PATH):
    """
    Reads a CSV file containing hotel data, sets the first column as the index,
    and returns the data as a dictionary of dictionaries.

    Args:
        hotels_path (str): Path to the hotels CSV file.

    Returns:
        dict: Same structure as get_landmarks().
    """
    df = pd.read_csv(hotels_path)
    hotels = []
    for idx, row in df.iterrows():
        hotel = Hotel(
            name=row['name'],
            lon=row['longitude'],
            lat=row['latitude']
        )
        hotels.append(hotel)
    return hotels


def get_time_matrix(time_matrix_path=TIME_MATRIX_PATH):
    """
    Reads a JSON file containing a time matrix and returns it as a dictionary.

    Args:
        time_matrix_path (str): Path to the time matrix JSON file."""
    time_matrix = pd.read_json(time_matrix_path, orient='index').to_dict()
    return time_matrix
