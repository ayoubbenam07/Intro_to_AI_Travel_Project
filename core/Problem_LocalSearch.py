import random
import math
from typing import List, Dict, Any
from core.Node_Classes import Landmark, Hotel

class TravelProblem_LocalSearch:
    """
    This class represents the travel guide problem formulation for Local Search algorithms.
    It manages state validation, neighbor generation, and state evaluation for a 24-hour trip.
    """

    def __init__(self, landmarks: List['Landmark'], travel_information: Dict[str, Any]):
        """
        Initializes the travel problem with landmarks and user preferences.

        Args:
            landmarks: A list of Landmark objects available to visit.
            travel_information: A dictionary containing user preferences and constraints.
                Expected keys:
                - 'hotel': Hotel object (starting and ending point).
                - 'Travel_day': three lettter string  (e.g., 'mon' , 'fri' ).
                - 'Travel_Time': float (Max travel time allowed in hours).
                - 'type_filter': list[str] (Allowed categories, e.g., ['Museum', 'Park']).
                - 'time_matrix': dict (Precomputed travel times in minutes between locations).
                - 'trip_start_time': int ( the starting hour of the trip )

        """
        if not landmarks:
            raise ValueError("No list of landmarks provided!")
        
        self.landmarks = landmarks
        self.landmarks_list = [landmark.name for landmark in landmarks]
        
        # Extract user preferences and constraints
        self.hotel = travel_information['hotel']
        self.Travel_day = travel_information['Travel_day']
        self.max_travel_time = travel_information['Travel_Time'] 
        if self.max_travel_time > 24 :
            raise ValueError("travel time should be less than 24 hours !")

      
        self.type_filter = travel_information['type_filter']

        self.trip_start_time = travel_information['trip_start_time']
        # Important: The time matrix must be passed in to calculate real road travel times
        self.time_matrix = travel_information['time_matrix']
        self.trip_start_time = travel_information['trip_start_time']

        # Generate the initial starting state (must be done AFTER setting rules)
        self.initial_state = self._generate_random_state()


    def valid_state(self, state: List['Landmark'], hard_constraints: bool = True, is_building: bool = False) -> bool:
        """
        Validates an itinerary based on time limits, opening hours, and category filters.
        Checks if the trip starts and ends at the hotel.
        """
        # 1. Quick Failure Checks: Null values or duplicate landmarks
        if not state:
            return False
        if None in state: 
            return False
        if len(set(lm.id for lm in state)) != len(state): 
            return False

        # Current time with minutes  
        current_time = self.trip_start_time * 60

        # 2. Iterate through the itinerary to track time and check constraints
        for i, landmark in enumerate(state):
            # Add travel time to get to this landmark
            if i == 0:
                # Travel from hotel to first landmark
                travel_mins = self.time_matrix[self.hotel.id][landmark.name]
               
            else:
                # Travel between landmarks
                travel_mins = self.time_matrix[state[i-1].name][landmark.name]
                            
            # Arrival time in minutes 
            current_time += travel_mins

            # Check if landmark is open at arrival
            if not landmark.is_open(self.Travel_day, (current_time % 1440)):
                return False
            
            if self.type_filter and landmark.landmark_type not in self.type_filter: 
                return False

              
            # Add the duration spent visiting the landmark (in minutes)
            current_time += landmark.visit_duration 

        # 3. Add the return trip to the hotel (Ensures it ends at hotel)
        return_mins = self.time_matrix[state[-1].name][self.hotel.id]
        current_time += return_mins 
        
        return_hour = current_time / 60
        
        # 4. Hard Constraint: Did the total trip exceed the user's allowed time?
        if hard_constraints:

            duration = return_hour - self.trip_start_time
            if duration > self.max_travel_time :        
                return False
            
            if not is_building:
                if duration < max(0, self.max_travel_time - 2):
                    return False
            
        return True
    


    def _generate_random_state(self) -> List['Landmark']:
        """
        Generates a valid, random initial state to kick off the search.
        
        """
        # using the landmark number if provided 
        

        # without using the landmark number    
        
        state = []

        failure = 0 
        while failure < 500: 
            try_state =  state.copy()
            item = random.choice(self.landmarks)
            if item not in state : 
                try_state.append(item)
            else :
                continue

            if not self.valid_state(try_state, is_building=True) : 
                    failure +=1 
                    continue
                
            state = try_state 
     
        return state
    

    
    def generate_neighbors(self, state: List['Landmark']) -> List[List['Landmark']]:
        """
        Generates all legally valid neighbors using two strategies:
        1. Replacement: Swapping an existing landmark for an unused one.
        2. Internal Swap: Changing the order of current landmarks.
        3. If the itinerary size is dynamic, also uses Add and Remove.
        """
        neighbors = set()
        current_ids = [landmark.id for landmark in state]

        # --- Strategy 1: Replacement Neighbors ---
        for i, landmark in enumerate(state):
            for new_item in self.landmarks:
                if new_item.id not in current_ids:
                    state_copy = state[:]  
                    state_copy[i] = new_item
                    
                    if self.valid_state(state_copy): 
                        neighbors.add(tuple(state_copy))

                        

        # --- Strategy 2: Internal Swap Neighbors ---
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                state_copy = state[:]
                # Swap the positions
                state_copy[i], state_copy[j] = state_copy[j], state_copy[i]
                
                if self.valid_state(state_copy):
                    neighbors.add(tuple(state_copy))


      
            
        # --- Strategy 3: ADD a landmark ---
        for new_item in self.landmarks:
                if new_item.id not in current_ids:
                    # Try inserting the new item at every possible step of the trip
                    # range(len(state) + 1) allows us to put it at the very start, middle, or very end
                    for insert_index in range(len(state) + 1):
                        state_copy = state[:]
                        state_copy.insert(insert_index, new_item)
                        
                        if self.valid_state(state_copy):
                            neighbors.add(tuple(state_copy))

        # --- Strategy 4: REMOVE a landmark ---
         # We should only allow removing if the trip has more than 1 stop left!
        if len(state) > 1:
                for i in range(len(state)):
                    state_copy = state[:]
                    state_copy.pop(i)  # Remove the landmark at index i
                    
                    if self.valid_state(state_copy):
                        neighbors.add(tuple(state_copy))            

        return [list(s) for s in neighbors]
    


    def _generate_random_neighbor(self, state: List['Landmark']) -> List['Landmark']:
        """Returns one random valid neighbor from the current state."""
        neighbors = self.generate_neighbors(state)
        # Fallback if no neighbors are found (rare, but prevents crashes)
        if not neighbors:
            return state 
        return random.choice(neighbors)
    


    def evaluate(self, state: List['Landmark']) -> float:
        """ 
        The Fitness Function. 
        Minimizes distance while heavily maximizing the interest score.
        A lower resulting float indicates a better itinerary.
        """
        total_rating = 0
        total_travel_time = 0 

        for i, landmark in enumerate(state):
            total_rating += landmark.interest_score
            
            # Travel time from hotel to first landmark, or between landmarks
            if i == 0:
                total_travel_time += self.time_matrix[self.hotel.id][landmark.name]
            else:
                
                total_travel_time += self.time_matrix[state[i-1].name][landmark.name]

        # Travel time  from final landmark back to the hotel
        total_travel_time += self.time_matrix[state[-1].name][self.hotel.id]

       
        #let the rating as the most importatn criteria 
        #the lower is better , it will be negative
        score =  total_travel_time -1000*total_rating
        
        return score
    
    def distance(self, loc1: Any, loc2: Any) -> float:
        """
        Calculates the Great-Circle (Haversine) distance
        Accepts both Landmark and Hotel objects (duck typing) since both have .lat and .lon.
        """
        
        # radius of earth in kilometers 
        R = 6371.0
        lat1 = math.radians(loc1.lat)
        lon1 = math.radians(loc1.lon)
        lat2 = math.radians(loc2.lat)
        lon2 = math.radians(loc2.lon)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos( lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance_km = R * c
        
        return distance_km
