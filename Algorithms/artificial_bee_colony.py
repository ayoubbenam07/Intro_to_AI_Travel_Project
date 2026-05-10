from core.Problem_LocalSearch import TravelProblem_LocalSearch
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Node_Classes import Landmark, Hotel
import math
import random


class Bee:
    def __init__(self, fitness: float, state: list[Landmark]):
        self.fitness = fitness
        self.state = state
        self.limit = 0


class ABC_Optimization:
    def __init__(
        self,
        problem: TravelProblem_LocalSearch,
        colony_ratio: float = 0.5,
        colony_size: int = 50,
        limit: int = 20,
        iterations: int = math.inf,
        selection_method: str = "roulette",
    ):
        self.problem = problem
        self.colony_size = colony_size
        self.colony_ratio = colony_ratio
        self.limit = limit
        self.iterations = iterations
        self.selection_method = selection_method
        self.employed_bee_number = math.ceil(self.colony_size * self.colony_ratio)
        self.onlooker_bee_number = self.colony_size - self.employed_bee_number
        print("eb : ", self.employed_bee_number, "ob : ", self.onlooker_bee_number)

        self.global_best_state = None
        self.global_best_fitness = -1
        self.population = []

        for bee in range(self.employed_bee_number):
            random_state = self.problem._generate_random_state()
            fitness = self.problem.evaluate(random_state)
            self.population.append(Bee(fitness, random_state))

        # Initialize global best with the best bee from initial population
        if self.population:
            best_initial_bee = max(self.population, key=lambda bee: bee.fitness)
            self.global_best_fitness = best_initial_bee.fitness
            self.global_best_state = best_initial_bee.state[:]

    def calculate_fitness(self, state):
        return self.problem.evaluate(state)

    def tournament_selection(self, tournament_size: int = 3):
        tournament_players = random.sample(self.population, tournament_size)
        winner = max(tournament_players, key=lambda player: player.fitness)

        return winner

    def roulette_wheel_selection(self):
        fitnesses = [bee.fitness for bee in self.population]
        min_fitness = min(fitnesses)

        if min_fitness < 0:
            weights = [f - min_fitness + 1e-6 for f in fitnesses]
        else:
            weights = [f + 1e-6 for f in fitnesses]

        winner = random.choices(self.population, weights=weights, k=1)[0]
        return winner

    def rank_selection(self):
        sorted_bees = sorted(self.population, key=lambda bee: bee.fitness)
        ranks = list(range(1, len(self.population) + 1))
        winner = random.choices(sorted_bees, weights=ranks, k=1)[0]
        return winner

    def _employed_bee_phase_(self):
        for bee in self.population:
            new_state = self.problem._generate_random_neighbor_fast(bee.state)
            new_fitness = self.calculate_fitness(new_state)

            if new_fitness > bee.fitness:
                bee.state = new_state
                bee.fitness = new_fitness
                bee.limit = 0

                if new_fitness > self.global_best_fitness:
                    self.global_best_fitness = new_fitness
                    self.global_best_state = new_state[:]

            else:
                bee.limit = bee.limit + 1

    def _onlooker_bee_phase_(self):
        for i in range(self.onlooker_bee_number):
            match self.selection_method:
                case "tournament":
                    target_bee = self.tournament_selection(3)
                case "roulette":
                    target_bee = self.roulette_wheel_selection()
                case "rank":
                    target_bee = self.rank_selection()
                case _:
                    target_bee = self.tournament_selection(3)

            new_state = self.problem._generate_random_neighbor_fast(target_bee.state)
            new_fitness = self.calculate_fitness(new_state)

            if new_fitness > target_bee.fitness:
                target_bee.state = new_state
                target_bee.fitness = new_fitness
                target_bee.limit = 0

                if new_fitness > self.global_best_fitness:
                    self.global_best_fitness = new_fitness
                    self.global_best_state = new_state[:]

            else:
                target_bee.limit = target_bee.limit + 1

    def _scout_bee_phase_(self):
        for bee in self.population:
            if bee.limit >= self.limit:
                new_state = self.problem._generate_random_state()
                new_fitness = self.calculate_fitness(new_state)

                bee.state = new_state
                bee.fitness = new_fitness
                bee.limit = 0

                if new_fitness > self.global_best_fitness:
                    self.global_best_fitness = new_fitness
                    self.global_best_state = new_state[:]

    def solve(self):
        current_iteration = 0
        while current_iteration < self.iterations:
            self._employed_bee_phase_()
            self._onlooker_bee_phase_()
            self._scout_bee_phase_()
            current_iteration = current_iteration + 1

        return self.global_best_state, self.global_best_fitness


# I love testing

# landmarks = get_landmarks()
# hotels = get_hotels()
# time_matrix = get_time_matrix()

# algiers_problem = TravelProblem_LocalSearch(landmarks, travel_information={ 'hotel': hotels[0], 'time_matrix': time_matrix, 'Travel_Time': 12, 'Travel_day': 'mon', 'trip_start_time': 8, 'type_filter': None })


# abc = ABC_Optimization(
#     problem=algiers_problem,
#     colony_ratio=0.5,
#     colony_size=40,
#     limit=20,
#     iterations=100,
#     selection_method="tournament"
# )

# global_best_state, global_best_fitness = abc.solve()

# print("Optimization Complete!")
# print("Final Best Score:", global_best_fitness)
# path = [l.name for l in global_best_state]
# print("Final Best Route:", path)
