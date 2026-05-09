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
        Higher is better (maximization).
        """
        if not self.problem.valid_state(state):
            return -float('inf')
        
        return self.problem.evaluate(state)

    def run(self) -> List[Landmark]:
        """
        Executes the Simulated Annealing search.
        Strictly follows the local search paradigm: moving from current state to neighbor.

        Returns:
            The best itinerary (list of Landmarks) found.
        """
        # Diversity memory (Tabu-lite) to avoid cycles within the local neighborhood
        tabu_list = []
        max_tabu_size = 20
        
        # Start at the provided initial state (Local Search requirement)
        current_state = self.problem.initial_state
        current_fitness = self.calculate_fitness(current_state)
        
        best_overall_state = current_state
        best_overall_fitness = current_fitness

        reheat_count = 0
        stagnation_counter = 0
        max_stagnation = 150 

        while reheat_count <= self.max_reheats:
            # Temperature acts as the probability threshold for accepting 'down-hill' moves
            self.temp = self.initial_temp * (1.0 / (reheat_count + 1)) 
            
            while self.temp > self.min_temp:
                # 1. Neighbor Generation: Explore the local neighborhood of the CURRENT state
                neighbors = self.problem.generate_neighbors(current_state)
                
                if not neighbors:
                    break

                # 2. Select a neighbor (using Tabu-lite to ensure we don't oscillate locally)
                valid_neighbors = [n for n in neighbors if tuple(lm.id for lm in n) not in tabu_list]
                neighbor = random.choice(valid_neighbors) if valid_neighbors else random.choice(neighbors)
                
                neighbor_fitness = self.calculate_fitness(neighbor)
                delta_e = current_fitness - neighbor_fitness # Maximization: current - neighbor

                # 3. Acceptance Criterion: Local search moves to a neighbor
                if delta_e < 0:
                    # Improvement move (neighbor is better)
                    current_state = neighbor
                    current_fitness = neighbor_fitness
                    stagnation_counter = 0 
                    
                    if current_fitness > best_overall_fitness:
                        best_overall_state = neighbor
                        best_overall_fitness = current_fitness
                else:
                    # Probabilistic move (Escape local optima)
                    # For maximization: P = exp(-(current - neighbor) / T)
                    acceptance_prob = math.exp(-delta_e / max(self.temp, 1e-10))
                    if random.random() < acceptance_prob:
                        current_state = neighbor
                        current_fitness = neighbor_fitness
                    
                    stagnation_counter += 1

                # Update Tabu List for local diversity
                state_id = tuple(lm.id for lm in current_state)
                tabu_list.append(state_id)
                if len(tabu_list) > max_tabu_size:
                    tabu_list.pop(0)

                # 4. Cooling: Move from exploration to exploitation
                if stagnation_counter == 0:
                    effective_cooling = 1.0 - (1.0 - self.cooling_rate) * 0.3 
                else:
                    effective_cooling = self.cooling_rate

                self.temp *= effective_cooling

                if stagnation_counter > max_stagnation:
                    break

            # 5. Reheating (Iterative Local Search): Restart from best or random to find new basins
            reheat_count += 1
            if reheat_count <= self.max_reheats:
                # To maintain local search integrity, we jump to a new starting point
                current_state = self.problem._generate_random_state()
                current_fitness = self.calculate_fitness(current_state)
                stagnation_counter = 0

        return best_overall_state

    def __str__(self):
        return f"Simulated Annealing (Best Fitness: {self.temp})"
