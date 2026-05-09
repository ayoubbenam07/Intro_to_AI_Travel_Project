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

    def __init__(
        self,
        id: int,
        name: str,
        lon: float,
        lat: float,
        interest_score: float,
        opening_hours: dict[str, list[int]],
        visit_duration: int,
        landmark_type: str,
    ):

        self.id = id
        self.name = name
        self.lon = lon
        self.lat = lat
        self.interest_score = interest_score
        self.opening_hours = opening_hours
        self.visit_duration = visit_duration
        self.landmark_type = landmark_type

    # check this , since we will be working with minutes and time matrix is in minutes we wont be doing conversion from min to hours

    def is_open(self, day: str, arrival_minutes: float) -> bool:
        """
        Checks if the landmark is open for the entire visit duration.
    
        Args:
            day(str): Day abbreviation e.g. 'mon', 'tue'
            arrival_minutes (float): Arrival time in minutes from midnight
                                    e.g. 540 = 09:00, 545.7 = 09:05:42

        Returns:
            bool: True if landmark is open for every hour slot of the visit
        """
        opening = self.opening_hours[day]
       
        if opening is None:
            print("no openning hour provided")
            return False

        finish_minutes = arrival_minutes + self.visit_duration

        # which hour slot do we arrive in?
        arrival_hour = int(arrival_minutes // 60)

        # which hour slot are we still INSIDE at the end?
        # subtract 1 so that finishing exactly on the hour (e.g. 600 = 10:00)
        # does not count as being inside the next slot (hour 10)
        finish_hour = int((finish_minutes - 1) // 60)

        for hour in range(arrival_hour, finish_hour + 1):
            if opening[hour % 24] == 0:
                
                return False
        
        return True


# this class represent single hotel


class Hotel:

    def __init__(self, name, lon, lat):
        self.id = name
        self.name = name
        self.lon = lon
        self.lat = lat
