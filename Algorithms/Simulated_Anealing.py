import random
import math
from typing import List, Optional
from core.Node_Classes import Landmark
from core.Problem_LocalSearch import TravelProblem_LocalSearch

class Simulated_Annealing:
    """
    Simulated Annealing implementation for the Travel Guide problem.
    Features: 
    - Adaptive Cooling
    - Reheating (Local Optima Escape)
    - Multi-stage search (Multi-restart with memory)
    """

    def __init__(self, problem: TravelProblem_LocalSearch, initial_temp: float = 100.0, cooling_rate: float = 0.98, min_temp: float = 0.001, max_reheats: int = 3):
        """
        Initializes the Simulated Annealing algorithm.

        Args:
            problem: An instance of TravelProblem_LocalSearch.
            initial_temp: The starting temperature for the annealing process.
            cooling_rate: The rate at which the temperature decreases.
            min_temp: The temperature at which the algorithm stops.
            max_reheats: Maximum number of times to perform reheating.
        """
        self.problem = problem
        self.initial_temp = initial_temp
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_reheats = max_reheats

    def calculate_fitness(self, state: List[Landmark]) -> float:
        """
        Calculates the fitness of a state by delegating to the problem's evaluate method.
        Lower is better (minimization).
        """
        if not self.problem.valid_state(state):
            return float('inf')
        
        return self.problem.evaluate(state)

    def run(self) -> List[Landmark]:
        """
        Executes the Simulated Annealing search.

        Returns:
            The best itinerary (list of Landmarks) found.
        """
        # Start with a random initial state from the problem
        current_state = self.problem.initial_state
        current_fitness = self.calculate_fitness(current_state)
        
        best_overall_state = current_state
        best_overall_fitness = current_fitness

        reheat_count = 0
        stagnation_counter = 0
        max_stagnation = 100 # Consecutive iterations without improvement

        while reheat_count <= self.max_reheats:
            self.temp = self.initial_temp * (1.0 / (reheat_count + 1)) # Scaled initial temp for reheats
            
            while self.temp > self.min_temp:
                # Generate neighbors
                neighbors = self.problem.generate_neighbors(current_state)
                
                if not neighbors:
                    break

                # Pick a random neighbor
                neighbor = random.choice(neighbors)
                neighbor_fitness = self.calculate_fitness(neighbor)

                delta_e = neighbor_fitness - current_fitness

                if delta_e < 0:
                    # Improvement
                    current_state = neighbor
                    current_fitness = neighbor_fitness
                    stagnation_counter = 0 
                    
                    if current_fitness < best_overall_fitness:
                        best_overall_state = neighbor
                        best_overall_fitness = current_fitness
                else:
                    # Acceptance Probability
                    # I am adding a small bias to the temperature to prevent division by zero and maintain search pressure
                    acceptance_prob = math.exp(-delta_e / max(self.temp, 1e-10))
                    
                    if random.random() < acceptance_prob:
                        current_state = neighbor
                        current_fitness = neighbor_fitness
                    
                    stagnation_counter += 1

                # Adaptive Cooling: slow down if I find improvements, speed up if stagnating
                if stagnation_counter == 0:
                    effective_cooling = 1.0 - (1.0 - self.cooling_rate) * 0.5 # Cool slower when improving
                else:
                    effective_cooling = self.cooling_rate

                self.temp *= effective_cooling

                # Early exit from this cycle if stagnating too long
                if stagnation_counter > max_stagnation:
                    break

            # Reheating logic: jump back to a higher temperature if I have reheats left
            reheat_count += 1
            if reheat_count <= self.max_reheats:
                # Perturb the best found state slightly to start the next cycle from a new perspective
                # Or start from a completely new random state to explore a different region
                current_state = self.problem._generate_random_state()
                current_fitness = self.calculate_fitness(current_state)
                stagnation_counter = 0

        return best_overall_state

    def __str__(self):
        return f"Simulated Annealing (Best Fitness: {self.temp})"
