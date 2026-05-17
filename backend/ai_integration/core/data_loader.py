"""
Data Loading Utilities
=======================
Loads landmarks, hotels, and time matrices from files
"""

import json
import csv
import os
from typing import List, Dict, Any
import numpy as np
from ai_integration.core.node_classes import Landmark, Hotel


# Cache for loaded data
_landmarks_cache = None
_hotels_cache = None
_time_matrix_cache = None

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')


def get_landmarks() -> List[Landmark]:
    """Load landmarks from CSV"""
    global _landmarks_cache
    if _landmarks_cache is not None:
        return _landmarks_cache
    
    landmarks = []
    csv_path = os.path.join(DATA_DIR, 'landmarks.csv')
    
    if not os.path.exists(csv_path):
        print(f"Warning: landmarks.csv not found at {csv_path}")
        return []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse opening hours JSON
            opening_hours = {}
            if 'Hours' in row and row['Hours']:
                try:
                    opening_hours = json.loads(row['Hours'])
                except:
                    opening_hours = {
                        'mon': [1]*24, 'tue': [1]*24, 'wed': [1]*24,
                        'thu': [1]*24, 'fri': [1]*24, 'sat': [1]*24, 'sun': [1]*24
                    }
            
            landmark = Landmark(
                landmark_id=row.get('ID', ''),
                name=row.get('Name', ''),
                description=row.get('Description', ''),
                landmark_type=row.get('Type', ''),
                rating=float(row.get('Rating', 5.0)),
                latitude=float(row.get('Latitude', 0.0)),
                longitude=float(row.get('Longitude', 0.0)),
                estimated_time=int(row.get('EstimatedTime (min)', 30)),
                opening_hours=opening_hours,
                image_url=row.get('Images', '')
            )
            landmarks.append(landmark)
    
    _landmarks_cache = landmarks
    return landmarks


def get_hotels() -> List[Hotel]:
    """Load hotels from CSV"""
    global _hotels_cache
    if _hotels_cache is not None:
        return _hotels_cache
    
    hotels = []
    csv_path = os.path.join(DATA_DIR, 'hotels.csv')
    
    if not os.path.exists(csv_path):
        print(f"Warning: hotels.csv not found at {csv_path}")
        return []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            hotel = Hotel(
                hotel_id=str(i),
                name=row.get('name', ''),
                latitude=float(row.get('latitude', 0.0)),
                longitude=float(row.get('longitude', 0.0))
            )
            hotels.append(hotel)
    
    _hotels_cache = hotels
    return hotels


def get_time_matrix() -> Dict[str, Dict[str, float]]:
    """Load time matrix from JSON"""
    global _time_matrix_cache
    if _time_matrix_cache is not None:
        return _time_matrix_cache
    
    json_path = os.path.join(DATA_DIR, 'time_matrix.json')
    
    if not os.path.exists(json_path):
        print(f"Warning: time_matrix.json not found at {json_path}")
        return {}
    
    with open(json_path, 'r', encoding='utf-8') as f:
        _time_matrix_cache = json.load(f)
    
    return _time_matrix_cache


def get_landmarks_from_db(db):
    """Load landmarks from database (for future database integration)"""
    # This is a placeholder for future database integration
    return get_landmarks()


def clear_cache():
    """Clear all loaded data caches"""
    global _landmarks_cache, _hotels_cache, _time_matrix_cache
    _landmarks_cache = None
    _hotels_cache = None
    _time_matrix_cache = None
