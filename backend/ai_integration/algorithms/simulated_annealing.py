"""
Simulated Annealing Algorithm
==============================
"""

import random
import math
from typing import List
from ai_integration.core.node_classes import Landmark
from ai_integration.core.problems import TravelProblem_LocalSearch


class Simulated_Annealing:
    """Simulated Annealing optimization for travel planning"""
    
    def __init__(
        self,
        problem: TravelProblem_LocalSearch,
        initial_temp: float = 100.0,
        cooling_rate: float = 0.98,
        min_temp: float = 0.001,
        max_reheats: int = 3
    ):
        self.problem = problem
        self.initial_temp = initial_temp
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_reheats = max_reheats
    
    def calculate_fitness(self, state: List[Landmark]) -> float:
        """Calculate fitness (higher is better)"""
        if not self.problem.valid_state(state):
            return -float('inf')
        return self.problem.evaluate(state)
    
    def run(self) -> List[Landmark]:
        """Execute Simulated Annealing"""
        current_state = self.problem.initial_state
        current_fitness = self.calculate_fitness(current_state)
        
        best_state = current_state
        best_fitness = current_fitness
        
        reheat_count = 0
        stagnation = 0
        max_stagnation = 150
        
        while reheat_count <= self.max_reheats:
            self.temp = self.initial_temp * (1.0 / (reheat_count + 1))
            
            while self.temp > self.min_temp:
                neighbors = self.problem.generate_neighbors(current_state)
                
                if not neighbors:
                    break
                
                neighbor = random.choice(neighbors)
                neighbor_fitness = self.calculate_fitness(neighbor)
                delta = neighbor_fitness - current_fitness
                
                # Maximization: accept if better OR with probability exp(delta/T)
                if delta > 0:
                    current_state = neighbor
                    current_fitness = neighbor_fitness
                    stagnation = 0
                    
                    if current_fitness > best_fitness:
                        best_state = neighbor
                        best_fitness = current_fitness
                else:
                    prob = math.exp(delta / max(self.temp, 1e-10))
                    if random.random() < prob:
                        current_state = neighbor
                        current_fitness = neighbor_fitness
                    stagnation += 1
                
                self.temp *= self.cooling_rate
                
                if stagnation > max_stagnation:
                    break
            
            reheat_count += 1
            if reheat_count <= self.max_reheats:
                current_state = self.problem._generate_random_state()
                current_fitness = self.calculate_fitness(current_state)
                stagnation = 0
        
        return best_state
