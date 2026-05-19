"""
Problem Formulation Classes
============================
Defines formal problem structures for different algorithm types
"""

from typing import List, Dict, Any, Tuple, Optional, Literal
import random
from ai_integration.core.node_classes import Landmark, Hotel


class TravelProblem_LocalSearch:
    """
    Problem definition for Local Search algorithms (SA, HC, GA, ABC).
    Handles state generation, neighbor generation, and evaluation.
    """
    
    def __init__(self, landmarks: List[Landmark], travel_information: Dict[str, Any]):
        """
        Args:
            landmarks: List of all available landmarks
            travel_information: Dict with keys:
                - 'hotel': Hotel object
                - 'Travel_day': day code ('mon', 'tue', etc.)
                - 'Travel_Time': max hours allowed (float)
                - 'type_filter': list of landmark types to include ([] = all)
                - 'time_matrix': dict of travel times
                - 'trip_start_time': hour of day to start (int)
        """
        if not landmarks:
            raise ValueError("No landmarks provided!")
        
        self.landmarks = landmarks
        self.hotel = travel_information['hotel']
        self.Travel_day = travel_information['Travel_day'].lower()[:3]
        self.max_travel_time = travel_information['Travel_Time']
        self.type_filter = travel_information.get('type_filter', [])
        self.time_matrix = travel_information['time_matrix']
        self.trip_start_time = travel_information['trip_start_time']
        
        if self.max_travel_time > 24:
            raise ValueError("travel time should be less than 24 hours!")
        
        # Apply type filter if specified
        if self.type_filter:
            self.landmarks = [
                lm for lm in landmarks
                if lm.landmark_type.lower() in [t.lower() for t in self.type_filter]
            ]
        
        self.initial_state = self._generate_random_state()
    
    def valid_state(self, state: List[Landmark], hard_constraints: bool = True, is_building: bool = False) -> bool:
        """Check if a state (itinerary) is valid"""
        if not state:
            return False
        if None in state:
            return False
        if len(set(lm.id for lm in state)) != len(state):
            return False
        
        current_time = self.trip_start_time * 60
        
        for i, landmark in enumerate(state):
            # Travel time to this landmark
            if i == 0:
                travel_mins = self.time_matrix[self.hotel.name][landmark.name]
            else:
                travel_mins = self.time_matrix[state[i-1].name][landmark.name]
            
            current_time += travel_mins
            
            # Check opening hours
            if not landmark.is_open(self.Travel_day, current_time % 1440):
                return False
            
            # Add visit duration
            current_time += landmark.visit_duration
        
        # Return to hotel
        return_mins = self.time_matrix[state[-1].name][self.hotel.name]
        current_time += return_mins
        
        return_hour = current_time / 60
        duration = return_hour - self.trip_start_time
        
        if hard_constraints and duration > self.max_travel_time:
            return False
        
        if not is_building and hard_constraints:
            if duration < max(0, self.max_travel_time - 2):
                if len(state) < len(self.landmarks):
                    return False
        
        return True
    
    def _generate_random_state(self) -> List[Landmark]:
        """Generate a valid random initial state"""
        state = []
        failures = 0
        
        while failures < 500:
            available = [lm for lm in self.landmarks if lm not in state]
            if not available:
                break
                
            try_state = state.copy()
            item = random.choice(available)
            try_state.append(item)
            
            if not self.valid_state(try_state, is_building=True):
                failures += 1
                continue
            
            state = try_state
            failures = 0
        
        return state
    
    def generate_neighbors(self, state: List[Landmark]) -> List[List[Landmark]]:
        """Generate neighboring states using SWAP and REPLACE operators"""
        neighbors = []
        current_ids = [landmark.id for landmark in state]
        
        # SWAP: exchange order of two landmarks
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                state_copy = state[:]
                state_copy[i], state_copy[j] = state_copy[j], state_copy[i]
                
                if self.valid_state(state_copy):
                    neighbors.append(state_copy)
        
        # REPLACE: swap landmark for unused one
        for i, landmark in enumerate(state):
            for new_item in self.landmarks:
                if new_item.id not in current_ids:
                    state_copy = state[:]
                    state_copy[i] = new_item
                    
                    if self.valid_state(state_copy):
                        neighbors.append(state_copy)
        
        return neighbors
    
    def evaluate(self, state: List[Landmark]) -> float:
        """Calculate fitness: (7 * total_rating) - total_travel_time"""
        if not self.valid_state(state):
            return -float('inf')
        
        total_rating = sum(lm.interest_score for lm in state)
        total_travel_time = 0.0
        
        # Travel from hotel to first landmark
        if state:
            total_travel_time += self.time_matrix[self.hotel.name][state[0].name]
            
            # Travel between landmarks
            for i in range(len(state) - 1):
                total_travel_time += self.time_matrix[state[i].name][state[i+1].name]
            
            # Return to hotel
            total_travel_time += self.time_matrix[state[-1].name][self.hotel.name]
        
        return (7.0 * total_rating) - total_travel_time


class TravelProblem_InformedSearch:
    """
    Problem definition for Informed Search algorithms (Greedy, A*).
    Uses states with tracking of visited landmarks and current time.
    """
    
    def __init__(
        self,
        hotel: Hotel,
        landmarks: List[Landmark],
        type_filter: List[str],
        time_matrix: Dict[str, Dict[str, float]],
        time_budget: int,  # minutes
        starting_time: int,  # minutes from midnight
        visiting_day: str,
    ):
        self.hotel = hotel
        
        # Apply type filter
        if len(type_filter) > 0:
            lower_filter = [t.lower() for t in type_filter]
            self.landmarks = [
                lm for lm in landmarks
                if lm.landmark_type.lower() in lower_filter
            ]
        else:
            self.landmarks = landmarks
        
        self.landmark_map = {l.name: l for l in landmarks}
        self.time_matrix = time_matrix
        self.time_budget = time_budget
        self.starting_time = starting_time
        self.end_time = starting_time + time_budget
        self.visiting_day = visiting_day
        
        # State: (current_position, visited_landmarks_frozenset, current_time)
        self.initial_state = (self.hotel.name, frozenset(), self.starting_time)
    
    def get_landmark_by_name(self, name: str) -> Optional[Landmark]:
        """Retrieve landmark by name"""
        return self.landmark_map.get(name)
    
    def actions(self, state: Tuple) -> List[Tuple[str, str]]:
        """Get all legal actions from a state"""
        current_position, visited_landmarks, current_time = state
        possible_actions = []
        
        for landmark in self.landmarks:
            if landmark.name in visited_landmarks:
                continue
            
            travel_forward = self.time_matrix[current_position][landmark.name]
            arrival_time = current_time + travel_forward
            
            travel_back = self.time_matrix[landmark.name][self.hotel.name]
            return_time = arrival_time + travel_back + landmark.visit_duration
            
            try:
                is_open = landmark.is_open(self.visiting_day, arrival_time)
            except KeyError:
                is_open = False
            
            if is_open and return_time <= self.end_time:
                possible_actions.append(("visit", landmark.name))
        
        if not possible_actions:
            possible_actions.append(("return", self.hotel.name))
        
        return possible_actions
    
    def result(self, state: Tuple, action: Tuple[str, str]) -> Tuple:
        """Apply action to state and return new state"""
        current_position, visited_landmarks, current_time = state
        travel_type, next_position = action
        
        travel_forward = self.time_matrix[current_position][next_position]
        new_visited_landmarks = visited_landmarks
        visit_duration = 0
        
        if travel_type == "visit":
            new_visited_landmarks = visited_landmarks | frozenset([next_position])
            visit_duration = self.get_landmark_by_name(next_position).visit_duration
        
        new_current_time = current_time + travel_forward + visit_duration
        return (next_position, new_visited_landmarks, new_current_time)
    
    def heuristic(self, parent_state: Tuple, child_state: Tuple) -> float:
        """Heuristic: (travel_forward + travel_back) / interest_score"""
        parent_position, _, _ = parent_state
        child_position, _, _ = child_state
        
        if child_position == self.hotel.name:
            return 0
        
        travel_forward = self.time_matrix[parent_position][child_position]
        travel_back = self.time_matrix[child_position][self.hotel.name]
        landmark_score = self.get_landmark_by_name(child_position).interest_score
        
        return (travel_forward + travel_back) / landmark_score if landmark_score > 0 else float('inf')
    
    def path_cost(self, state: Tuple) -> int:
        """Return elapsed minutes since trip start"""
        _, _, current_time = state
        return current_time - self.starting_time
