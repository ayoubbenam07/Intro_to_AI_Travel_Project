from Node import Landmark, Hotel

class TravelProblem_InformedSearch:
    def __init__(
        self,
        hotel: Hotel,
        landmarks: list[Landmark],
        time_matrix: dict[str, dict[str, float]],
        time_budget: int,
        starting_time: int,
        visiting_day: str,
    ):
        self.hotel = hotel
        self.landmarks = landmarks
        self.landmark_map = {l.name: l for l in landmarks}
        self.time_matrix = time_matrix
        self.time_budget = time_budget
        self.starting_time = starting_time
        self.visiting_day = visiting_day
        self.initial_state = (self.hotel.name, frozenset(), self.starting_time) # (Current Position, Dict of visited, Current time)
 
    def get_landmark_by_name(self, name):
        return self.landmark_map.get(name)
    
    def actions(self, state):
        current_position, visited_landmarks, current_time = state
        possible_actions = []

        for landmark in self.landmarks:
            if landmark in visited_landmarks:
                continue
            
            travel_forward = self.time_matrix[current_position][landmark.name]
            arrival_time = current_time + travel_forward
            travel_back = self.time_matrix[landmark.name][self.hotel.name]
            return_time = arrival_time + travel_back + landmark.visit_duration

            deadline = self.starting_time + self.time_budget

            if (landmark.is_open(self.visiting_day, arrival_time) and return_time <= deadline):
                possible_actions.append(('visit', landmark.name))
        
        possible_actions.append(('return', self.hotel.name))
        return possible_actions
    
    def result(self, state, action):
        current_position, visited_landmarks, current_time = state
        travel_type, next_position = action

        travel_forward = self.time_matrix[current_position][next_position]
        new_visited_landmarks = visited_landmarks
        visit_duration = 0

        if travel_type == "visit":
            new_visited_landmarks = visited_landmarks | frozenset([next_position])
            landmark = self.get_landmark_by_name(next_position)
            visit_duration = landmark.visit_duration

        new_current_time = current_time + travel_forward + visit_duration

        return (next_position, new_visited_landmarks, new_current_time)
        

    def heuristic(self, state, landmark : Landmark):
        current_position, _, _ = state

        travel_forward = self.time_matrix[current_position][landmark.name]
        travel_back = self.time_matrix[landmark.name][self.hotel.name]
        landmark_score = landmark.interest_score

        return (travel_forward + travel_back) / landmark_score