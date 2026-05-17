"""
Hill Climbing Algorithm
=======================
"""

import random
from typing import List
from ai_integration.core.node_classes import Landmark
from ai_integration.core.problems import TravelProblem_LocalSearch


class hill_climbing:
    """Hill Climbing optimization for travel planning"""
    
    def __init__(
        self,
        problem: TravelProblem_LocalSearch,
        num_restarts: int = 1,
        base_strategy: str = "steepest"
    ):
        self.problem = problem
        self.base_strategy = base_strategy
        self.num_restarts = num_restarts
    
    def evaluate(self, state: List[Landmark]) -> float:
        """Evaluate state fitness"""
        return self.problem.evaluate(state)
    
    def search(self) -> List[Landmark]:
        """Single hill climbing search"""
        current_state = self.problem.initial_state
        current_value = self.evaluate(current_state)
        
        if self.base_strategy == "steepest":
            while True:
                neighbors = self.problem.generate_neighbors(current_state)
                
                if not neighbors:
                    break
                
                best_neighbor = None
                best_value = current_value
                
                for neighbor in neighbors:
                    neighbor_value = self.evaluate(neighbor)
                    if neighbor_value > best_value:
                        best_neighbor = neighbor
                        best_value = neighbor_value
                
                if best_neighbor is None:
                    break
                
                current_state = best_neighbor
                current_value = best_value
        
        elif self.base_strategy == "stochastic":
            while True:
                neighbors = self.problem.generate_neighbors(current_state)
                
                if not neighbors:
                    break
                
                better_neighbors = []
                for neighbor in neighbors:
                    if self.evaluate(neighbor) > current_value:
                        better_neighbors.append(neighbor)
                
                if not better_neighbors:
                    break
                
                current_state = random.choice(better_neighbors)
                current_value = self.evaluate(current_state)
        
        elif self.base_strategy == "first_choice":
            while True:
                neighbors = self.problem.generate_neighbors(current_state)
                found = False
                
                for neighbor in neighbors:
                    if self.evaluate(neighbor) > current_value:
                        current_state = neighbor
                        current_value = self.evaluate(current_state)
                        found = True
                        break
                
                if not found:
                    break
        
        return current_state
    
    def run(self) -> List[Landmark]:
        """Execute hill climbing with restarts"""
        best_state = None
        best_value = -float('inf')
        
        for _ in range(self.num_restarts):
            state = self.search()
            value = self.evaluate(state)
            
            if value > best_value:
                best_state = state
                best_value = value
        
        return best_state
