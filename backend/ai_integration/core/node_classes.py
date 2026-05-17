"""
Node Classes for Travel Guide Problem
======================================
Defines the domain entities: Hotel and Landmark
"""

from typing import Dict, Optional
import math


class Hotel:
    """Represents a hotel (start/end point of the trip)"""
    
    def __init__(self, hotel_id: str, name: str, latitude: float, longitude: float):
        self.id = hotel_id
        self.name = name
        self.lat = latitude
        self.lon = longitude
    
    def __repr__(self):
        return f"Hotel({self.name}, {self.lat}, {self.lon})"
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Hotel):
            return self.id == other.id
        return False


class Landmark:
    """Represents a landmark (point of interest to visit)"""
    
    def __init__(
        self,
        landmark_id: str,
        name: str,
        description: str,
        landmark_type: str,
        rating: float,
        latitude: float,
        longitude: float,
        estimated_time: int,
        opening_hours: Dict[str, list],
        image_url: str = ""
    ):
        self.id = landmark_id
        self.name = name
        self.description = description
        self.landmark_type = landmark_type
        self.rating = rating
        self.lat = latitude
        self.lon = longitude
        self.visit_duration = estimated_time  # minutes
        self.opening_hours = opening_hours  # dict: day -> [24 binary flags]
        self.image_url = image_url
        
        # Interest score: combine rating with estimated time to reflect value
        self.interest_score = rating
    
    def __repr__(self):
        return f"Landmark({self.name}, {self.landmark_type})"
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Landmark):
            return self.id == other.id
        return False
    
    def is_open(self, day: str, arrival_time_minutes: float) -> bool:
        """
        Check if landmark is open at the given arrival time.
        
        Args:
            day: 3-letter day code (mon, tue, ..., sun)
            arrival_time_minutes: minutes from midnight (0-1440)
        
        Returns:
            True if landmark is open at arrival time
        """
        if day not in self.opening_hours:
            return False
        
        hours = self.opening_hours[day]
        if hours is None:
            return False
        
        hour = int(arrival_time_minutes // 60)
        if hour >= 24:
            return False
        
        return hours[hour % 24] == 1
