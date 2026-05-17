"""
Artificial Bee Colony (ABC) Algorithm
======================================
"""

import random
import math
from typing import List
from ai_integration.core.node_classes import Landmark
from ai_integration.core.problems import TravelProblem_LocalSearch


class Bee:
    """Represents a bee with a food source (solution)"""
    
    def __init__(self, fitness: float, state: List[Landmark]):
        self.fitness = fitness
        self.state = state
        self.limit = 0


class ABC_Optimization:
    """Artificial Bee Colony optimizer"""
    
    def __init__(
        self,
        problem: TravelProblem_LocalSearch,
        colony_ratio: float = 0.5,
        colony_size: int = 60,
        limit: int = 20,
        iterations: int = 100,
        selection_method: str = "rank"
    ):
        self.problem = problem
        self.colony_size = colony_size
        self.colony_ratio = colony_ratio
        self.limit = limit
        self.iterations = iterations
        self.selection_method = selection_method
        
        self.employed_bee_number = math.ceil(colony_size * colony_ratio)
        self.onlooker_bee_number = colony_size - self.employed_bee_number
        
        self.global_best_state = None
        self.global_best_fitness = -float('inf')
        self.population = []
        
        # Initialize population
        for _ in range(self.employed_bee_number):
            state = problem._generate_random_state()
            fitness = problem.evaluate(state)
            self.population.append(Bee(fitness, state))
        
        if self.population:
            best_bee = max(self.population, key=lambda b: b.fitness)
            self.global_best_fitness = best_bee.fitness
            self.global_best_state = best_bee.state[:]
    
    def calculate_fitness(self, state: List[Landmark]) -> float:
        """Calculate fitness"""
        return self.problem.evaluate(state)
    
    def tournament_selection(self, tournament_size: int = 3) -> Bee:
        """Tournament selection"""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda b: b.fitness)
    
    def roulette_wheel_selection(self) -> Bee:
        """Fitness-proportionate selection"""
        fitnesses = [max(0, bee.fitness) for bee in self.population]
        total = sum(fitnesses)
        
        if total <= 0:
            return random.choice(self.population)
        
        pick = random.uniform(0, total)
        cumulative = 0
        
        for bee, fitness in zip(self.population, fitnesses):
            cumulative += fitness
            if cumulative >= pick:
                return bee
        
        return self.population[-1]
    
    def rank_selection(self) -> Bee:
        """Rank-based selection"""
        sorted_pop = sorted(self.population, key=lambda b: b.fitness, reverse=True)
        ranks = list(range(len(self.population), 0, -1))
        return random.choices(sorted_pop, weights=ranks)[0]
    
    def solve(self) -> List[Landmark]:
        """Execute ABC algorithm"""
        for iteration in range(self.iterations):
            # Employed bee phase
            for bee in self.population:
                neighbor_state = random.choice(self.problem.generate_neighbors(bee.state))
                neighbor_fitness = self.calculate_fitness(neighbor_state)
                
                if neighbor_fitness > bee.fitness:
                    bee.state = neighbor_state
                    bee.fitness = neighbor_fitness
                    bee.limit = 0
                    
                    if bee.fitness > self.global_best_fitness:
                        self.global_best_fitness = bee.fitness
                        self.global_best_state = bee.state[:]
                else:
                    bee.limit += 1
            
            # Onlooker bee phase
            for _ in range(self.onlooker_bee_number):
                if self.selection_method == "roulette":
                    selected_bee = self.roulette_wheel_selection()
                elif self.selection_method == "rank":
                    selected_bee = self.rank_selection()
                else:
                    selected_bee = self.tournament_selection()
                
                neighbor_state = random.choice(self.problem.generate_neighbors(selected_bee.state))
                neighbor_fitness = self.calculate_fitness(neighbor_state)
                
                if neighbor_fitness > selected_bee.fitness:
                    selected_bee.state = neighbor_state
                    selected_bee.fitness = neighbor_fitness
                    selected_bee.limit = 0
                    
                    if selected_bee.fitness > self.global_best_fitness:
                        self.global_best_fitness = selected_bee.fitness
                        self.global_best_state = selected_bee.state[:]
                else:
                    selected_bee.limit += 1
            
            # Scout bee phase: replace abandoned sources
            for bee in self.population:
                if bee.limit >= self.limit:
                    bee.state = self.problem._generate_random_state()
                    bee.fitness = self.calculate_fitness(bee.state)
                    bee.limit = 0
        
        return self.global_best_state if self.global_best_state else self.problem.initial_state
