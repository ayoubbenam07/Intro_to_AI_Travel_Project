import random
import math
from typing import List, Tuple, Set, Union
from core.Node_Classes import Landmark, Hotel
from core.Problem_AntColony import ACSEnvironment
from Algorithms.Simulated_Anealing import Simulated_Annealing
from core.Problem_LocalSearch import TravelProblem_LocalSearch

# PS: The notes underneath are just a clarification of how we will use the hybrid ACS-SA, we will remove them before submission (if I forget please do instead of me!)
class Ant:
    """
    Represents a single 'tourist' agent building an itinerary step-by-step.
    """
    
    def __init__(self, environment: ACSEnvironment) -> None:
        """
        Initializes the ant at the Hotel at the starting time.
        
        Args:
            environment (ACSEnvironment): The map and memory state.
        """
        self.env: ACSEnvironment = environment
        self.current_node: Union[Hotel, Landmark] = self.env.hotel
        self.current_time: float = self.env.starting_time

        # Use a set for lightning-fast O(1) lookups of visited locations
        self.visited: Set[str] = {self.env.hotel.name}    
        
        # Track the actual trip path and the total accumulated score
        self.path: List[Union[Hotel, Landmark]] = [self.env.hotel] 
        self.total_score: float = 0.0

    def build_trip(self, alpha: float, beta: float) -> None:
        """
        Loops continuously, moving the ant from landmark to landmark until time runs out.
        
        Args:
            alpha (float): Trust in the pheromone herd memory.
            beta (float): Trust in personal heuristic logic (distance/rating).
        """
        while True:
            # 1. Ask the environment where we can legally go
            valid_moves = self.env.get_valid_next_moves(self.current_node, self.current_time, self.visited)
            
            # If no moves are left, the trip is over! Go back to the hotel.
            if not valid_moves:
                time_to_home = self.env.get_travel_time(self.current_node, self.env.hotel)
                self.current_time += time_to_home
                self.path.append(self.env.hotel)
                break
                
            # 2. Pick the next location using probabilistic loaded dice
            next_landmark = self._choose_next_node(valid_moves, alpha, beta)
            
            # 3. Physically move the ant there and update constraints
            travel_time = self.env.get_travel_time(self.current_node, next_landmark)
            
            self.current_time += (travel_time + next_landmark.visit_duration)
            self.current_node = next_landmark
            self.visited.add(next_landmark.name)
            self.path.append(next_landmark)
            
            # Add the rating to the total score
            self.total_score += next_landmark.interest_score

    def _choose_next_node(self, valid_moves: List[Landmark], alpha: float, beta: float) -> Landmark:
        """
        Calculates the probabilities of moving to each valid landmark and selects one.
        
        Args:
            valid_moves (List[Landmark]): Allowed next destinations.
            alpha (float): Pheromone weight.
            beta (float): Heuristic logic weight.
            
        Returns:
            Landmark: The selected next destination.
        """
        probabilities: List[Tuple[Landmark, float]] = []
        total_desirability: float = 0.0
        
        # Calculate the raw desirability of every valid move
        for landmark in valid_moves:
            # Pheromone (The Herd's memory)
            tau = self.env.matrix[self.current_node.name][landmark.name]
            
            # Heuristic (The Ant's logic: High Rating + Short Distance = Good!)
            travel_time = self.env.get_travel_time(self.current_node, landmark)
          
            # CORRECTED ETA MATH: Divide by travel time so closer places get higher desirability scores!
            # Added + 1.0 to prevent dividing by zero if locations are identical.

            eta = landmark.interest_score / math.sqrt((travel_time + 1.0)) 
       
            
            # Combine them using Alpha and Beta
            desirability = (tau ** alpha) * (eta ** beta)
            probabilities.append((landmark, desirability))
            total_desirability += desirability
            
        # Convert desirability into actual percentages (Roulette Wheel Selection)
        random_spin = random.uniform(0, total_desirability)
        cumulative: float = 0.0
        
        for landmark, desirability in probabilities:
            cumulative += desirability
            if cumulative >= random_spin:
                return landmark
                
        # Fallback (should rarely happen due to float rounding)
        return probabilities[-1][0]


class AntColonySystem:
    """
    The master orchestrator that manages generations, spawns ants, and tracks the global best trip.
    """
    
    def __init__(
        self, 
        environment: ACSEnvironment, 
        num_ants: int = 30, 
        generations: int = 100, 
        alpha: float = 1.0, 
        beta: float = 2.5, 
        rho: float = 0.1,
        hybrid_sa: bool = False
    ) -> None:
        """
        Initializes the solver.
        
        Args:
            environment (ACSEnvironment): The map instance.
            num_ants (int): Number of ants per generation (default 30).
            generations (int): Total iterations to run (default 100).
            alpha (float): Pheromone importance.
            beta (float): Heuristic importance (set higher than alpha for time windows).
            rho (float): Pheromone evaporation rate.
            hybrid_sa (bool): Whether to use Simulated Annealing for local refinement.
        """
        self.env: ACSEnvironment = environment
        self.num_ants: int = num_ants
        self.generations: int = generations
        self.hybrid_sa: bool = hybrid_sa
        
        self.alpha: float = alpha  
        self.beta: float = beta    
        self.rho: float = rho      
        
        # Memory of the absolute best trip ever found across all generations
        self.global_best_path: List[Union[Hotel, Landmark]] = []
        self.global_best_score: float = -1.0

    def solve(self) -> Tuple[List[Union[Hotel, Landmark]], float]:
        """
        Executes the Ant Colony System loop.
        
        Returns:
            Tuple[List[Hotel|Landmark], float]: The optimal itinerary and its total score.
        """
        print(f"Starting Ant Colony System for {self.generations} generations...")
        
        for gen in range(self.generations):
            generation_trips: List[Tuple[List[Union[Hotel, Landmark]], float]] = []
            
            # 1. Spawn all ants and let them build trips
            for _ in range(self.num_ants):
                ant = Ant(self.env)
                ant.build_trip(self.alpha, self.beta)
                
                path = ant.path
                score = ant.total_score
                
                # HYBRID FEATURE: If enabled, refine the ant's trip using Simulated Annealing
                if self.hybrid_sa:
                    refined_path = self._refine_with_sa(path)
                    # Note: We need a way to recalculate score if SA found a better path
                    # For now, we update score if path changed
                    if refined_path != path:
                        path = refined_path
                        # Score is recalculated based on the refined path interest
                        score = sum(lm.interest_score for lm in path if isinstance(lm, Landmark))

                generation_trips.append((path, score))
                
                # Check if this ant or its refined version beat the all-time world record
                if score > self.global_best_score:
                    self.global_best_score = score
                    self.global_best_path = path

    def _refine_with_sa(self, path: List[Union[Hotel, Landmark]]) -> List[Union[Hotel, Landmark]]:
        """
        Optional local refinement using the Simulated Annealing algorithm.
        """
        # Strip hotels for the local search problem which often expects just landmarks
        landmarks_only = [node for node in path if isinstance(node, Landmark)]
        
        if not landmarks_only:
            return path
            
        # Create a temporary local search problem context for this ant's path
        # Assuming environment has a travel_info attribute or similar to reconstruct the problem
        try:
            # This part requires access to the original problem parameters
            # If the environment stores the travel_information dictionary:
            travel_info = self.env.travel_info 
            problem = TravelProblem_LocalSearch(self.env.all_landmarks, travel_info)
            problem.initial_state = landmarks_only
            
            # Run a 'lite' version of SA for speed (less reheats, faster cooling)
            sa = Simulated_Annealing(problem, initial_temp=50.0, cooling_rate=0.95, max_reheats=1)
            refined_landmarks = sa.run()
            
            # Reconstruct the full path with hotels
            return [self.env.hotel] + refined_landmarks + [self.env.hotel]
        except Exception:
            # Fallback if problem reconstruction fails
            return path

    def solve(self) -> Tuple[List[Union[Hotel, Landmark]], float]:
        """
        Executes the Ant Colony System loop.
        
        Returns:
            Tuple[List[Hotel|Landmark], float]: The optimal itinerary and its total score.
        """
        print(f"Starting Ant Colony System for {self.generations} generations...")
        
        for gen in range(self.generations):
            generation_trips: List[Tuple[List[Union[Hotel, Landmark]], float]] = []
            
            # 1. Spawn all ants and let them build trips
            for _ in range(self.num_ants):
                ant = Ant(self.env)
                ant.build_trip(self.alpha, self.beta)
                
                path = ant.path
                score = ant.total_score
                
                # HYBRID FEATURE: If enabled, refine the ant's trip using Simulated Annealing
                if self.hybrid_sa:
                    refined_path = self._refine_with_sa(path)
                    # Note: We need a way to recalculate score if SA found a better path
                    # For now, we update score if path changed
                    if refined_path != path:
                        path = refined_path
                        # Score is recalculated based on the refined path interest
                        score = sum(lm.interest_score for lm in path if isinstance(lm, Landmark))

                generation_trips.append((path, score))
                
                # Check if this ant or its refined version beat the all-time world record
                if score > self.global_best_score:
                    self.global_best_score = score
                    self.global_best_path = path
                    
            # 2. Sort today's trips from best to worst
            generation_trips.sort(key=lambda x: x[1], reverse=True)
            
            # 3. Take the top 5 ants of this generation to drop pheromones (Rank-based)
            top_5_trips = generation_trips[:5]
            
            # 4. Tell the environment to fade old smells and drop new ones
            self.env.evaporate_and_reinforce(top_5_trips, rho=self.rho)
            
            # Optional: Print progress dynamically
            if (gen + 1) % 10 == 0:
                print(f"Generation {gen + 1} | Current Best Score: {self.global_best_score:.2f}")
                
        print("\nOptimization Complete!")
        return self.global_best_path, self.global_best_score