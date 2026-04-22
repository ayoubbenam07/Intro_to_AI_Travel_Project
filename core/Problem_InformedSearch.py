from Node import Landmark, Hotel


class TravelProblem_InformedSearch:
    def __init__(
        self,
        hotel: Hotel,
        landmarks: list[Landmark],
        time_matrix: dict[str, dict[str, float]],
        time_badget: int,
        starting_time: int,
    ):
        self.hotel = hotel
        self.landmarks = landmarks
        self.time_matrix = time_matrix
        self.time_badget = time_badget
        self.starting_time = starting_time
        self.initial_state = (hotel, {})
        return
