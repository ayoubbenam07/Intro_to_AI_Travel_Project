"""
Ant Colony System Environment
==============================
Defines the environment for ACS algorithm
"""

from typing import List, Dict, Union, Set
import math
from ai_integration.core.node_classes import Landmark, Hotel


class ACSEnvironment:
    """Environment for Ant Colony System algorithm"""
    
    def __init__(
        self,
        hotel: Hotel,
        landmarks: List[Landmark],
        type_filter: List[str],
        time_matrix: Dict[str, Dict[str, float]],
        time_budget: float,  # hours
        starting_time: float,  # hour of day
        visiting_day: str,
    ):
        self.hotel = hotel
        self.time_budget = time_budget * 60  # convert to minutes
        self.starting_time = starting_time * 60  # convert to minutes
        self.visiting_day = visiting_day.lower()[:3]
        self.time_matrix = time_matrix
        
        # Apply type filter
        if type_filter:
            self.landmarks = [
                lm for lm in landmarks
                if lm.landmark_type.lower() in [t.lower() for t in type_filter]
            ]
        else:
            self.landmarks = landmarks
        
        self.all_landmarks = landmarks  # keep unfiltered for reference
        
        # Initialize pheromone matrix: τ[i][j] = initial pheromone on edge i→j
        # Higher τ = more desirable edge
        self.matrix = self._initialize_pheromone_matrix()
    
    def _initialize_pheromone_matrix(self) -> Dict[str, Dict[str, float]]:
        """Initialize pheromone levels for all edges"""
        matrix = {}
        
        # Add hotel
        all_names = [self.hotel.name] + [lm.name for lm in self.landmarks]
        
        for name1 in all_names:
            matrix[name1] = {}
            for name2 in all_names:
                if name1 != name2:
                    # Initial pheromone: inversely proportional to distance/time
                    travel_time = self.time_matrix.get(name1, {}).get(name2, 100)
                    if travel_time > 0:
                        matrix[name1][name2] = 1.0 / travel_time
                    else:
                        matrix[name1][name2] = 1.0
                else:
                    matrix[name1][name2] = 0.0
        
        return matrix
    
    def get_travel_time(self, from_node: Union[Hotel, Landmark], to_node: Union[Hotel, Landmark]) -> float:
        """Get travel time between two nodes"""
        return self.time_matrix.get(from_node.name, {}).get(to_node.name, 100)
    
    def get_valid_next_moves(
        self,
        current_node: Union[Hotel, Landmark],
        current_time: float,
        visited: Set[str]
    ) -> List[Landmark]:
        """
        Get list of valid next landmarks from current position.
        
        A landmark is valid if:
        1. Not already visited
        2. Open at arrival time
        3. Can fit in time budget (visit + return)
        """
        valid_moves = []
        
        for landmark in self.landmarks:
            # Skip if already visited
            if landmark.name in visited:
                continue
            
            # Calculate travel and arrival time
            travel_time = self.get_travel_time(current_node, landmark)
            arrival_time = current_time + travel_time
            
            # Check if open at arrival
            try:
                if not landmark.is_open(self.visiting_day, arrival_time % 1440):
                    continue
            except KeyError:
                continue
            
            # Check if can return to hotel within budget
            return_time = self.get_travel_time(landmark, self.hotel)
            finish_time = arrival_time + landmark.visit_duration + return_time
            
            if finish_time <= self.starting_time + self.time_budget:
                valid_moves.append(landmark)
        
        return valid_moves
    
    def update_pheromone(
        self,
        path: List[Union[Hotel, Landmark]],
        score: float,
        evaporation_rate: float = 0.1
    ):
        """Update pheromone levels based on ant's path"""
        # Evaporate
        for i in self.matrix:
            for j in self.matrix[i]:
                self.matrix[i][j] *= (1 - evaporation_rate)
        
        # Deposit pheromone along the path
        if not path or score <= 0:
            return
        
        deposit = score / 100.0  # Normalize deposit
        
        for i in range(len(path) - 1):
            u_name = path[i].name
            v_name = path[i + 1].name
            
            if u_name in self.matrix and v_name in self.matrix[u_name]:
                self.matrix[u_name][v_name] += deposit
