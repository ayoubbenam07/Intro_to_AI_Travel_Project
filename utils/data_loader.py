import pandas as pd
from pathlib import Path

# .resolve() guarantees a full absolute path
_BASE_DIR = Path(__file__).resolve().parent.parent

# Path to CSV files 
LANDMARKS_PATH = _BASE_DIR / "dataset" / "landmarks" / "Algiers_landmarks.csv"
HOTELS_PATH = _BASE_DIR / "dataset" / "hotels" / "Algiers_hotels.csv"

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
    df.set_index(df.columns[0], inplace=True)
    return df.to_dict(orient='index') 

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
    df.set_index(df.columns[0], inplace=True)
    return df.to_dict(orient='index')