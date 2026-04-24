
class Landmark:

    """
    Represents a single tourist landmark or attraction.
    
    Attributes:
        id (int): A unique numerical identifier for the landmark.
        name (str): The name of the landmark.
        lon (float): Longitude coordinate.
        lat (float): Latitude coordinate.
        interest_score (float): The rating or user interest score.
        opening_hours (dict[str, list[int]]): A dictionary mapping days of the week 
            (e.g., 'Monday') to a list of 24 integers representing hours. 
            1 means open, 0 means closed. Example: {'Monday': [0,0,...,1,1,0]}
        visit_duration (int): Estimated time spent at the landmark in minutes.
        landmark_type (str): The category of the landmark (e.g., 'Museum', 'Park').
    """

    def __init__(self, id: int, name: str, lon: float, lat: float, 
                 interest_score: float, opening_hours: dict[str, list[int]], 
                 visit_duration: int, landmark_type: str):
        
        self.id = id
        self.name = name
        self.lon = lon
        self.lat = lat
        self.interest_score = interest_score
        self.opening_hours = opening_hours
        self.visit_duration = visit_duration
        self.landmark_type = landmark_type

    def is_open(self, day: str, hour: int) -> bool:
        """
        Checks if the landmark remains open for the entire duration of a planned visit.
        
        Args:
            day (str): The day of the week to check (e.g., 'Monday').
            hour (int): The starting hour of the visit (0-23).
            
        Returns:
            bool: True if the landmark is open for every hour of the visit, False otherwise.
        """
        # Retrieve the 24-hour schedule for the specified day
        opening = self.opening_hours.get(day)
        
        # Failsafe: if the day doesn't exist in the dictionary, assume it's closed
        if not opening:
            return False

        # Calculate how many hours the visit will take (rounded up to be safe)
        duration_in_hours = int(self.visit_duration / 60)
        
        # Check every hour from the arrival time to the departure time
        for i in range(hour, hour + duration_in_hours + 1):
            
            # i % 24 ensures that hour 24 wraps back to 0 (midnight)
            if opening[i % 24] == 0:
                return False 

        return True
    




#this class represent single hotel

class Hotel:

    def __init__(self , name , lon, lat ):
      self.id = name
      self.lon = lon
      self.lat = lat 


