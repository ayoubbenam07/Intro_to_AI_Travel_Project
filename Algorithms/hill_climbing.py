import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from core.Node_Classes import Landmark, Hotel
from typing import List

class Candidate:
    def __init__(self, state, value):
        self.state = state
        self.value = value

    def __repr__(self):
        state_repr = str(self.state)
        if len(state_repr) > 50:
            state_repr = state_repr[:47] + "..."
        value_repr = f"{self.value:.4f}" if isinstance(self.value, float) else str(self.value)
        return f"Candidate(state={state_repr}, value={value_repr})"

class hill_climbing:
    def __init__(self, problem:TravelProblem_LocalSearch, num_restarts=1, base_strategy="steepest"):
        self.problem = problem
        self.base_strategy = base_strategy
        self.num_restarts=num_restarts

    def generate_random_initial_state(self):
        trip_start_time = self.problem.trip_start_time
        shuffled = self.problem.landmarks[:]
        random.shuffle(shuffled)
        
        initial_state = []
        current_time = trip_start_time * 60  

        for landmark in shuffled:
            # 1. Calculate travel time
            if not initial_state:
                travel_mins = self.problem.time_matrix[self.problem.hotel.id][landmark.name]
            else:
                travel_mins = self.problem.time_matrix[initial_state[-1].name][landmark.name]

            arrival_time = current_time + travel_mins

            # 2. Check opening hours and waiting logic
            if not landmark.is_open(self.problem.Travel_day, arrival_time % 1440):
                opening = landmark.opening_hours[self.problem.Travel_day]
                if opening is None:
                    continue
                
                hour = int(arrival_time // 60) + 1
                waited = False
                while hour < 24:
                    if opening[hour % 24] == 1:
                        wait_arrival = hour * 60
                        return_mins = self.problem.time_matrix[landmark.name][self.problem.hotel.id]
                        finish_time = wait_arrival + landmark.visit_duration + return_mins
                        
                        if (finish_time / 60) - trip_start_time <= self.problem.max_travel_time:
                            arrival_time = wait_arrival
                            waited = True
                        break
                    hour += 1
                if not waited:
                    continue

            # 3. Check type filters
            if self.problem.type_filter and landmark.landmark_type not in self.problem.type_filter:
                continue

            # 4. Check if we can make it back to the hotel in time
            return_mins = self.problem.time_matrix[landmark.name][self.problem.hotel.id]
            finish_time = arrival_time + landmark.visit_duration + return_mins
            
            if (finish_time / 60) - trip_start_time > self.problem.max_travel_time:
                continue

            # 5. Add to state
            initial_state.append(landmark)
            current_time = arrival_time + landmark.visit_duration
        return initial_state
    
    def evaluate(self, state: List['Landmark']) -> float:
        if not self.problem.valid_state(state):
            return float('-inf') 
        total_time_hours = self.calculate_total_time(state)
        total_interest = sum(landmark.interest_score for landmark in state)
        if total_time_hours > self.problem.max_travel_time:
            time_overage = total_time_hours - self.problem.max_travel_time
            penalty = time_overage * 0.1 
            evaluation_rate = total_interest - penalty
        else:
            evaluation_rate = total_interest
        
        return evaluation_rate

    def generate_first_best_neighbors(self, state: List['Landmark']):
        """
        Generates all legally valid neighbors using two strategies:
        1. Replacement: Swapping an existing landmark for an unused one.
        2. Internal Swap: Changing the order of current landmarks.
        3. If the itinerary size is dynamic, also uses Add and Remove.
        Yields neighbors one by one to allow stopping early.
        """
        neighbors = set()
        current_ids = [landmark.id for landmark in state]

        # --- Strategy 1: Replacement Neighbors ---
        for i, landmark in enumerate(state):
            for new_item in self.problem.landmarks:
                if new_item.id not in current_ids:
                    state_copy = state[:]  
                    state_copy[i] = new_item
                    
                    if self.problem.valid_state(state_copy): 
                        neighbor_tuple = tuple(state_copy)
                        if neighbor_tuple not in neighbors:
                            neighbors.add(neighbor_tuple)
                            yield list(state_copy)

                        

        # --- Strategy 2: Internal Swap Neighbors ---
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                state_copy = state[:]
                # Swap the positions
                state_copy[i], state_copy[j] = state_copy[j], state_copy[i]
                
                if self.problem.valid_state(state_copy):
                    neighbor_tuple = tuple(state_copy)
                    if neighbor_tuple not in neighbors:
                        neighbors.add(neighbor_tuple)
                        yield list(state_copy)


        # --- Dynamic Strategies: ADD and REMOVE ---
        if not self.problem.Landmarks_number:
            
            # --- Strategy 3: ADD a landmark ---
            for new_item in self.problem.landmarks:
                if new_item.id not in current_ids:
                    # Try inserting the new item at every possible step of the trip
                    # range(len(state) + 1) allows us to put it at the very start, middle, or very end
                    for insert_index in range(len(state) + 1):
                        state_copy = state[:]
                        state_copy.insert(insert_index, new_item)
                        
                        if self.problem.valid_state(state_copy):
                            neighbor_tuple = tuple(state_copy)
                            if neighbor_tuple not in neighbors:
                                neighbors.add(neighbor_tuple)
                                yield list(state_copy)

            # --- Strategy 4: REMOVE a landmark ---
            # We should only allow removing if the trip has more than 1 stop left!
            if len(state) > 1:
                for i in range(len(state)):
                    state_copy = state[:]
                    state_copy.pop(i)  # Remove the landmark at index i
                    
                    if self.problem.valid_state(state_copy):
                        neighbor_tuple = tuple(state_copy)
                        if neighbor_tuple not in neighbors:
                            neighbors.add(neighbor_tuple)
                            yield list(state_copy)

    def calculate_total_time(self, state) -> float:
        if not state:
            return 0
        total_time = self.problem.time_matrix[self.problem.hotel.id][state[0].name]
        for i, landmark in enumerate(state):
            total_time += landmark.visit_duration
            if i < len(state) - 1:
                total_time += self.problem.time_matrix[landmark.name][state[i + 1].name]
        total_time += self.problem.time_matrix[state[-1].name][self.problem.hotel.id]
        return total_time / 60

    def search(self):
        current_state = self.generate_random_initial_state()
        current_value = self.evaluate(current_state)
        current_candidate = Candidate(current_state, current_value)

        if self.base_strategy == "steepest":
            while True:
                neighbors = self.problem.generate_neighbors(current_candidate.state)

                best_neighbor_candidate = None

                if not neighbors:
                    break

                for neighbor in neighbors:
                    neighbor_value = self.evaluate(neighbor)

                    if best_neighbor_candidate == None or neighbor_value > best_neighbor_candidate.value:
                        best_neighbor_candidate = Candidate(neighbor, neighbor_value)

                if best_neighbor_candidate.value > current_candidate.value:
                    current_candidate = best_neighbor_candidate
                else:
                    break
        
        elif self.base_strategy == "stochastic":
            while True:
                neighbors = self.problem.generate_neighbors(current_candidate.state)

                best_neighbor_candidates = []

                if not neighbors:
                    break

                for neighbor in neighbors:
                    neighbor_value = self.evaluate(neighbor)

                    if neighbor_value > current_candidate.value:
                        best_neighbor_candidates.append(Candidate(neighbor, neighbor_value)) 

                if not best_neighbor_candidates:
                    break

                current_candidate = random.choice(best_neighbor_candidates)

        elif self.base_strategy == "first_choice":
            while True:
                first_best_neighbor_candidate = None

                for neighbor in self.generate_first_best_neighbors(current_candidate.state):
                    neighbor_value = self.evaluate(neighbor)

                    if neighbor_value > current_candidate.value:
                        first_best_neighbor_candidate = Candidate(neighbor, neighbor_value)
                        break

                if first_best_neighbor_candidate is None:
                    break
                else:
                    current_candidate = first_best_neighbor_candidate

        return current_candidate
    
    def run(self):
        best_candidate_overall = None

        for i in range(self.num_restarts):
            candidate_this_restart = self.search()
            if best_candidate_overall is None or candidate_this_restart.value > best_candidate_overall.value:
                best_candidate_overall = candidate_this_restart
        
        return best_candidate_overall



# landmarks = get_landmarks()
# hotels = get_hotels()
# time_matrix = get_time_matrix()

# problem = TravelProblem_LocalSearch(landmarks, travel_information={ 'hotel': hotels[0], 'time_matrix': time_matrix, 'Travel_Time': 12, 'Travel_day': 'fri', 'type_filter': None, 'Landmarks_number': None , 'trip_start_time': 8})

# base_strategies = ['steepest', 'stochastic', 'first_choice']
# num_restarts = [1, 50,100]

# for strategy in base_strategies:
#     print("="*50)
#     print(f"Running Hill Climbing with strategy: {strategy}")
#     for restarts in num_restarts:
#         print("-"*50)
#         print(f"Number of restarts: {restarts}")
#         hc = hill_climbing(problem, num_restarts=restarts, base_strategy=strategy)
#         best_solution = hc.run()
#         print(hc.evaluate(best_solution.state))
#         print("Best Itinerary:", hotels[0].name, [landmark.name for landmark in best_solution.state], "\nTotal Interest Score:", sum(landmark.interest_score for landmark in best_solution.state), "\nTotal Time:", round(hc.calculate_total_time(best_solution.state), 2), '\nNumber of Landmarks:', len(best_solution.state))