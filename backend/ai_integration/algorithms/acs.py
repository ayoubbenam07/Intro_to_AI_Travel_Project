"""
Ant Colony System (ACS)
=======================
"""

import random
import math
from typing import List, Union, Set
from ai_integration.core.node_classes import Landmark, Hotel
from ai_integration.core.acs_environment import ACSEnvironment


class Ant:
    """Single ant building a solution"""
    
    def __init__(self, environment: ACSEnvironment):
        self.env = environment
        self.current_node: Union[Hotel, Landmark] = environment.hotel
        self.current_time: float = environment.starting_time
        self.visited: Set[str] = {environment.hotel.name}
        self.path: List[Union[Hotel, Landmark]] = [environment.hotel]
        self.total_score: float = 0.0
    
    def build_trip(self, alpha: float, beta: float) -> None:
        """Build trip by visiting landmarks"""
        while True:
            valid_moves = self.env.get_valid_next_moves(self.current_node, self.current_time, self.visited)
            
            if not valid_moves:
                time_to_home = self.env.get_travel_time(self.current_node, self.env.hotel)
                self.current_time += time_to_home
                self.path.append(self.env.hotel)
                break
            
            next_landmark = self._choose_next_node(valid_moves, alpha, beta)
            
            travel_time = self.env.get_travel_time(self.current_node, next_landmark)
            self.current_time += (travel_time + next_landmark.visit_duration)
            self.current_node = next_landmark
            self.visited.add(next_landmark.name)
            self.path.append(next_landmark)
            self.total_score += next_landmark.interest_score
    
    def _choose_next_node(self, valid_moves: List[Landmark], alpha: float, beta: float) -> Landmark:
        """Choose next node probabilistically based on pheromone and heuristic"""
        probabilities = []
        total_desirability = 0.0
        
        for landmark in valid_moves:
            tau = self.env.matrix[self.current_node.name][landmark.name]
            travel_time = self.env.get_travel_time(self.current_node, landmark)
            eta = landmark.interest_score / math.sqrt(travel_time + 1.0)
            
            desirability = (tau ** alpha) * (eta ** beta)
            probabilities.append((landmark, desirability))
            total_desirability += desirability
        
        if total_desirability <= 0:
            return random.choice(valid_moves)
        
        random_spin = random.uniform(0, total_desirability)
        cumulative = 0.0
        
        for landmark, desirability in probabilities:
            cumulative += desirability
            if cumulative >= random_spin:
                return landmark
        
        return probabilities[-1][0]


class AntColonySystem:
    """Ant Colony System optimizer"""
    
    def __init__(
        self,
        environment: ACSEnvironment,
        num_ants: int = 50,
        generations: int = 100,
        alpha: float = 0.5,
        beta: float = 3.0,
        rho: float = 0.05,
        hybrid_sa: bool = False
    ):
        self.env = environment
        self.num_ants = num_ants
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.hybrid_sa = hybrid_sa
        
        self.global_best_path: List[Union[Hotel, Landmark]] = []
        self.global_best_score: float = -1.0
    
    def solve(self) -> List[Landmark]:
        """Execute ACS"""
        for gen in range(self.generations):
            generation_trips = []
            
            for _ in range(self.num_ants):
                ant = Ant(self.env)
                ant.build_trip(self.alpha, self.beta)
                
                path = ant.path
                score = ant.total_score
                generation_trips.append((path, score))
                
                if score > self.global_best_score:
                    self.global_best_score = score
                    self.global_best_path = path[:]
            
            # Sort by score descending
            generation_trips.sort(key=lambda x: x[1], reverse=True)
            
            # Update pheromone from top ants
            for i, (path, score) in enumerate(generation_trips[:5]):
                weight = 5 - i  # Rank-based weights
                self.env.update_pheromone(path, score * weight, evaporation_rate=self.rho)
        
        # Extract only landmarks from path (skip hotel)
        landmarks_only = [node for node in self.global_best_path if isinstance(node, Landmark)]
        return landmarks_only
