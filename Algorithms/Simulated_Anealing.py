import random
import math
from typing import List, Optional
from core.Node_Classes import Landmark
from core.Problem_LocalSearch import TravelProblem_LocalSearch

class Simulated_Annealing:
    """
    Simulated Annealing implementation for the Travel Guide problem.
    It uses a cooling schedule to exploration and exploitation of the search space.
    """

    def __init__(self, problem: TravelProblem_LocalSearch, initial_temp: float = 100.0, cooling_rate: float = 0.95, min_temp: float = 0.01):
        """
        Initializes the Simulated Annealing algorithm.

        Args:
            problem: An instance of TravelProblem_LocalSearch.
            initial_temp: The starting temperature for the annealing process.
            cooling_rate: The rate at which the temperature decreases (linear/exponential reduction).
            min_temp: The temperature at which the algorithm stops.
        """
        self.problem = problem
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp

    def calculate_fitness(self, state: List[Landmark]) -> float:
        """
        Calculates the fitness of a state by delegating to the problem's evaluate method.
        
        Note: The problem.evaluate() method in this project returns a value to be minimized
        (lower is better), combining interest scores and travel time.
        """
        if not self.problem.valid_state(state):
            return float('inf') # Return infinity for invalid states (minimization)
        
        return self.problem.evaluate(state)

    def run(self) -> List[Landmark]:
        """
        Executes the Simulated Annealing search.

        Returns:
            The best itinerary (list of Landmarks) found.
        """
        current_state = self.problem.initial_state
        current_fitness = self.calculate_fitness(current_state)
        
        best_state = current_state
        best_fitness = current_fitness

        while self.temp > self.min_temp:
            # neighbors:
            neighbors = self.problem.generate_neighbors(current_state)
            
            if not neighbors:
                break

            # Pick a random neighbor
            neighbor = random.choice(neighbors)
            neighbor_fitness = self.calculate_fitness(neighbor)

            # Task 3: Acceptance Logic using Boltzmann Probability formula (P = e^-deltaE/T)
            # For minimization: deltaE = (Neighbor Fitness - Current Fitness)
            # If neighbor is better (neighbor < current), deltaE is negative, P > 1 (always accept)
            # If neighbor is worse (neighbor > current), deltaE is positive, P = e^(-deltaE/T)
            
            delta_e = neighbor_fitness - current_fitness

            if delta_e < 0:
                # Better solution found, always accept
                current_state = neighbor
                current_fitness = neighbor_fitness
                
                # Update global best
                if current_fitness < best_fitness:
                    best_state = neighbor
                    best_fitness = neighbor_fitness
            else:
                # Worse solution, accept with Boltzmann Probability P = e^(-ΔE/T)
                acceptance_prob = math.exp(-delta_e / self.temp)
                if random.random() < acceptance_prob:
                    current_state = neighbor
                    current_fitness = neighbor_fitness



            # Cool down
            self.temp *= self.cooling_rate

        return best_state

    def __str__(self):
        return f"Simulated Annealing (Temp: {self.temp}, Cooling: {self.cooling_rate})"
