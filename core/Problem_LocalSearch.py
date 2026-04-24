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
                - 'Travel_day': three lettter string  (e.g., 'Mon' , 'Fri' ).
                - 'Travel_Time': float (Max travel time allowed in hours).
                - 'Landmarks_number': int (Number of landmarks the user wants to visit).
                - 'type_filter': list[str] (Allowed categories, e.g., ['Museum', 'Park']).
                - 'time_matrix': dict (Precomputed travel times in minutes between locations).
        """
        if not landmarks:
            raise ValueError("No list of landmarks provided!")
        
        self.landmarks = landmarks
        self.landmarks_list = [landmark.name for landmark in landmarks]
        
        # Extract user preferences and constraints
        self.hotel = travel_information['hotel']
        self.Travel_day = travel_information['Travel_day']
        self.max_travel_time = travel_information['Travel_Time']  
        self.Landmarks_number = travel_information['Landmarks_number']
        self.type_filter = travel_information['type_filter']
        
        # Important: The time matrix must be passed in to calculate real road travel times
        self.time_matrix = travel_information['time_matrix']

        # Generate the initial starting state (must be done AFTER setting rules)
        self.initial_state = self._generate_random_state()


    def valid_state(self, state: List['Landmark'], hard_constraints: bool = True) -> bool:
        """
        Validates an itinerary based on time limits, opening hours, and category filters.
        """
        # 1. Quick Failure Checks: Null values or duplicate landmarks
        if not state:
            return False
        if None in state: 
            return False
        if len(set(lm.id for lm in state)) != len(state): 
            return False
        
        trip_start_time = 8.0  # Assuming trips start at 8:00 AM and we can change it if we want

        #current time with minutes  
        current_time  = trip_start_time*60
        
        # 2. Iterate through the itinerary to track time and check constraints
        for i, landmark in enumerate(state):
            
            # Add travel time to get to this landmark
            if i == 0:
                travel_mins = self.time_matrix[self.hotel.id][landmark.name]
            else:
                travel_mins = self.time_matrix[state[i-1].name][landmark.name]
                           
             #arrival time in minutes 
            current_time += travel_mins

            # Check if landmark is open at arrival and exit times  
            if not landmark.is_open(self.Travel_day, current_time ): 
                return False
            
            if self.type_filter and landmark.landmark_type not in self.type_filter: 
                return False
                
            # Add the duration spent visiting the landmark ( in minutes )
            current_time += landmark.visit_duration 

        # 3. Add the return trip to the hotel
        return_mins = self.time_matrix[state[-1].name][self.hotel.id]
        
        current_time += return_mins 
        
        return_hour = current_time/60
        # 4. Hard Constraint: Did the total trip exceed the user's allowed time?
        if hard_constraints:
            if (return_hour - trip_start_time) > self.max_travel_time:
                return False
            
        return True
    


    def _generate_random_state(self) -> List['Landmark']:
        """
        Generates a valid, random initial state to kick off the search.
        
        """
        # using the landmark number if provided 
        if self.Landmarks_number : 
            state = [None for _ in range(self.Landmarks_number)]

            attempts = 0

            # Keep rolling until we find a combination that passes all constraints
            while not self.valid_state(state) and attempts < 1000:
                state = [random.choice(self.landmarks) for _ in range(self.Landmarks_number)] 
                attempts+=1

            if (attempts >  1000):raise ValueError("constraints for generation invalid")


        # without using the landmark number    
        else :
            state = []

            failure = 0 
            while failure < 10: 
                try_state =  state[:]
                item = random.choice(self.landmarks)
                if item not in state : try_state.append(item)
                if not self.valid_state(try_state) : 
                    failure +=1 
                    continue
                
                state  = try_state                      


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


        # --- Dynamic Strategies: ADD and REMOVE ---
        if not self.Landmarks_number:
            
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
