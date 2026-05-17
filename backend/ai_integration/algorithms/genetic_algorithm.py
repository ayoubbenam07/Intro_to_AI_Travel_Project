"""
Genetic Algorithm
=================
"""

import random
from typing import List, Tuple
from ai_integration.core.node_classes import Landmark
from ai_integration.core.problems import TravelProblem_LocalSearch


class Genetic_Algorithm:
    """Genetic Algorithm for travel planning"""
    
    def __init__(
        self,
        problem: TravelProblem_LocalSearch,
        population_size: int = 100,
        generations: int = 80,
        mutation_rate: float = 0.1
    ):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.generate_population()
    
    def generate_population(self) -> List[List[Landmark]]:
        """Generate initial population of valid solutions"""
        population = []
        for _ in range(self.population_size):
            state = self.problem._generate_random_state()
            if self.problem.valid_state(state):
                population.append(state)
        
        return population if population else [self.problem.initial_state]
    
    def calculate_fitness(self, individual: List[Landmark]) -> float:
        """Calculate fitness"""
        return self.problem.evaluate(individual)
    
    def tournament_selection(self, tournament_size: int = 3) -> List[Landmark]:
        """Tournament selection"""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=self.calculate_fitness)
    
    def order_crossover(self, parent1: List[Landmark], parent2: List[Landmark]) -> Tuple[List[Landmark], List[Landmark]]:
        """Order (OX) crossover for permutation"""
        if len(parent1) < 2 or len(parent2) < 2:
            return parent1[:], parent2[:]
        
        limit = min(len(parent1), len(parent2))
        p1, p2 = sorted(random.sample(range(limit), 2))
        
        # Child 1
        child1 = [None] * len(parent1)
        child1[p1:p2] = parent1[p1:p2]
        used1 = set(parent1[p1:p2])
        
        idx = 0
        for i in range(len(child1)):
            if child1[i] is None:
                while idx < len(parent2) and parent2[idx] in used1:
                    idx += 1
                if idx < len(parent2):
                    child1[i] = parent2[idx]
                    used1.add(parent2[idx])
                    idx += 1
        
        child1 = [g for g in child1 if g is not None]
        
        # Child 2 (similar logic)
        child2 = [None] * len(parent2)
        child2[p1:p2] = parent2[p1:p2]
        used2 = set(parent2[p1:p2])
        
        idx = 0
        for i in range(len(child2)):
            if child2[i] is None:
                while idx < len(parent1) and parent1[idx] in used2:
                    idx += 1
                if idx < len(parent1):
                    child2[i] = parent1[idx]
                    used2.add(parent1[idx])
                    idx += 1
        
        child2 = [g for g in child2 if g is not None]
        
        return child1, child2
    
    def scramble_mutation(self, individual: List[Landmark]) -> List[Landmark]:
        """Scramble mutation: shuffle a segment"""
        if len(individual) < 2:
            return individual
        
        mutant = individual[:]
        i, j = sorted(random.sample(range(len(mutant)), 2))
        segment = mutant[i:j+1]
        random.shuffle(segment)
        mutant[i:j+1] = segment
        return mutant
    
    def evolve(self, selection_method: str = "tournament", crossover_method: str = "order", mutation_method: str = "scramble") -> List[Landmark]:
        """Execute genetic algorithm"""
        for generation in range(self.generations):
            fitness_scores = [self.calculate_fitness(ind) for ind in self.population]
            
            new_population = []
            
            for _ in range(self.population_size // 2):
                # Selection
                if selection_method == "tournament":
                    parent1 = self.tournament_selection()
                    parent2 = self.tournament_selection()
                else:
                    parent1 = random.choice(self.population)
                    parent2 = random.choice(self.population)
                
                # Crossover
                if crossover_method == "order":
                    child1, child2 = self.order_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1[:], parent2[:]
                
                # Mutation
                if random.random() < self.mutation_rate:
                    if mutation_method == "scramble":
                        child1 = self.scramble_mutation(child1)
                        child2 = self.scramble_mutation(child2)
                
                # Validation and addition
                if self.problem.valid_state(child1):
                    new_population.append(child1)
                if self.problem.valid_state(child2):
                    new_population.append(child2)
            
            # Keep best from previous generation
            sorted_pop = sorted(self.population, key=self.calculate_fitness, reverse=True)
            self.population = sorted_pop[:self.population_size - len(new_population)] + new_population
        
        # Return best individual
        return max(self.population, key=self.calculate_fitness)
