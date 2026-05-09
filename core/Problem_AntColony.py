from typing import List, Dict, Tuple, Set, Union
from core.Node_Classes import Landmark, Hotel

class ACSEnvironment:
    """
    Acts as the 'Map' or 'Game Engine' for the Ant Colony System.
    Manages the travel times, time constraints, and the Pheromone Matrix memory.
    """

    def __init__(
        self,
        hotel: Hotel,
        landmarks: List[Landmark],
        time_matrix: Dict[str, Dict[str, float]],
        time_budget_hours: float,    
        trip_start_time_hours: float, 
        visiting_day: str,
    ) -> None:
        """
        Initializes the Ant Colony Environment.
        
        Args:
            hotel (Hotel): The starting and ending location of the trip.
            landmarks (List[Landmark]): A list of all available Landmark objects.
            time_matrix (Dict[str, Dict[str, float]]): 2D dictionary of travel times in minutes.
            time_budget_hours (float): Total allowed duration of the trip in hours.
            trip_start_time_hours (float): Starting time of the trip (0.0 to 23.99).
            visiting_day (str): The day of the week (e.g., 'mon', 'tue').
        """
        self.hotel: Hotel = hotel
        self.landmarks: List[Landmark] = landmarks
        self.time_matrix: Dict[str, Dict[str, float]] = time_matrix

        # Convert time units from hours to minutes for internal calculations
        self.time_budget: float = time_budget_hours * 60.0 
        self.starting_time: float = trip_start_time_hours * 60.0 
        self.visiting_day: str = visiting_day.lower()
        
        # Initialize the Pheromone Matrix
        self.matrix: Dict[str, Dict[str, float]] = self._initialize_pheromones()

    def _initialize_pheromones(self) -> Dict[str, Dict[str, float]]:
        """
        Creates the memory bank for the ants. Uses node names as dictionary keys.
        
        Returns:
            Dict[str, Dict[str, float]]: A 2D dictionary initialized with default pheromone levels (1.0).
        """
        matrix: Dict[str, Dict[str, float]] = {}
        all_nodes: List[Union[Hotel, Landmark]] = [self.hotel] + self.landmarks
        
        for from_node in all_nodes:
            matrix[from_node.name] = {}
            for to_node in all_nodes:
                if from_node.name != to_node.name:
                    matrix[from_node.name][to_node.name] = 1.0 # Default baseline smell
        return matrix

    def get_travel_time(self, from_node: Union[Hotel, Landmark], to_node: Union[Hotel, Landmark]) -> float:
        """
        Retrieves the travel time between two nodes.
        
        Args:
            from_node (Hotel | Landmark): The starting node object.
            to_node (Hotel | Landmark): The destination node object.
            
        Returns:
            float: The travel time in minutes.
        """
        return self.time_matrix[from_node.name][to_node.name]

    def get_valid_next_moves(
        self, 
        current_node: Union[Hotel, Landmark], 
        current_time_minutes: float, 
        visited_objects: Set[str]
    ) -> List[Landmark]:
        """
        The 'Bouncer': Evaluates all landmarks and returns only the ones that can be legally visited.
        
        Args:
            current_node (Hotel | Landmark): Where the ant currently is.
            current_time_minutes (float): The ant's current clock time.
            visited_objects (Set[str]): A set containing the names of already visited nodes.
            
        Returns:
            List[Landmark]: A filtered list of Landmark objects that are open and reachable.
        """
        valid_moves: List[Landmark] = []
        
        for landmark in self.landmarks:
            if landmark.name in visited_objects:
                continue
                
            travel_time = self.get_travel_time(current_node, landmark)
            arrival_time = current_time_minutes + travel_time
            
            # Check if landmark is open upon arrival and for the duration of the visit
            if not landmark.is_open(self.visiting_day, arrival_time):
                continue
                
            time_after_visit = arrival_time + landmark.visit_duration
            time_to_get_home = self.get_travel_time(landmark, self.hotel)
            
            # Check if ant can complete the visit and return to hotel before budget expires
            if (time_after_visit + time_to_get_home) <= (self.starting_time + self.time_budget):
                valid_moves.append(landmark)
                
        return valid_moves
        
    def evaporate_and_reinforce(self, top_trips: List[Tuple[List[Union[Hotel, Landmark]], float]], rho: float = 0.1, tau_min: float = 0.01) -> None:
        """
        Updates the Pheromone Matrix at the end of a generation.
        
        Args:
            top_trips (List[Tuple[List, float]]): The best trips of the generation, sorted by score.
            rho (float): The evaporation rate (percentage of pheromone lost). Default is 0.1 (10%).
            tau_min (float): The absolute minimum pheromone level allowed to force exploration.
        """
        # 1. Evaporate all trails
        for from_name in self.matrix:
            for to_name in self.matrix[from_name]:
                self.matrix[from_name][to_name] *= (1.0 - rho)
                
                # Apply the Pheromone Floor to prevent division by zero or permanent dead ends
                if self.matrix[from_name][to_name] < tau_min:
                    self.matrix[from_name][to_name] = tau_min
                    
        # 2. Reinforce the TOP ants
        # FIX: Since trips contain 15-20 landmarks, total scores can reach 150-200.
        # A Q of 0.05 scales a massive score of 200 down to a healthy pheromone drop of 10.0.
        Q: float = 0.05 
        weight: float = 1.0 # The #1 ant drops 100%, #2 drops 80%, etc.
        
        for trip_objects, score in top_trips:
            pheromone_drop = (Q * score) * weight 
            
            for i in range(len(trip_objects) - 1):
                from_name = trip_objects[i].name
                to_name = trip_objects[i+1].name
                self.matrix[from_name][to_name] += pheromone_drop
                
            # Decrease the weight for the next ant down the leaderboard
            weight *= 0.8