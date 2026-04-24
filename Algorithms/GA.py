# impelemnt everything in details with docuementations and comments

import random
from typing import List, Literal
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from core.Node_Classes import Landmark, Hotel


class Genetic_Algorithm:
    def __init__(self, problem: TravelProblem_LocalSearch, population_size: int, generations: int, mutation_rate: float):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.generate_population()

    def __str__(self):
        return f"Genetic Algorithm with population size {self.population_size}, generations {self.generations}, and mutation rate {self.mutation_rate}"
    

    # Generating Population

    def generate_population(self):
          
        population = []
        trip_start_time = 8.0  
        for _ in range(self.population_size):
            shuffled = self.problem.landmarks[:]
            random.shuffle(shuffled)
            individual = []
            current_time = trip_start_time * 60  

            for landmark in shuffled:
                if not individual:
                    travel_mins = self.problem.time_matrix[self.problem.hotel.id][landmark.name]
                else:
                    travel_mins = self.problem.time_matrix[individual[-1].name][landmark.name]

                arrival_time = current_time + travel_mins

                # If closed at arrival, try waiting until it opens
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

                if self.problem.type_filter and landmark.landmark_type not in self.problem.type_filter:
                    continue

                return_mins = self.problem.time_matrix[landmark.name][self.problem.hotel.id]
                finish_time = arrival_time + landmark.visit_duration + return_mins
                if (finish_time / 60) - trip_start_time > self.problem.max_travel_time:
                    continue

                individual.append(landmark)
                current_time = arrival_time + landmark.visit_duration

            population.append(individual)
        return population

    # Fitness Function

    def calculate_fitness(self, individual: List['Landmark']) -> float:
        if not self.is_valid_individual(individual):
            return float('-inf')    
        total_time = self.calculate_total_time(individual)
        total_interest = sum(landmark.interest_score for landmark in individual)
        if total_time > self.problem.max_travel_time:
            fitness = total_interest / (1 + total_time - self.problem.max_travel_time)
        else:
            fitness = total_interest  
        
        return fitness



    # Selection Methods

    def tournament_selection(self, tournament_size: int):
        tournament_players = random.sample(self.population, tournament_size)
        winner = tournament_players[0]
        winner_fitness = self.calculate_fitness(winner)
        for player in tournament_players[1:]:
            if self.calculate_fitness(player) > winner_fitness:
                winner = player
        return winner
        


    def roulette_wheel_selection(self):
        fitnesses = [max(0, self.calculate_fitness(individual)) for individual in self.population]
        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            return random.choice(self.population)
        R = random.uniform(0, total_fitness)
        cumulative_fitness = 0
        for individual, fitness in zip(self.population, fitnesses):
            cumulative_fitness += fitness
            if cumulative_fitness >= R:
                return individual
        return self.population[-1]


    def rank_selection(self):
        fitnesses = [self.calculate_fitness(individual) for individual in self.population]
        sorted_population = [x for _, x in sorted(zip(fitnesses, self.population), key=lambda pair: pair[0])]
        total_sum = self.population_size * (self.population_size + 1) / 2
        R = random.uniform(0, total_sum)
        cumulative_sum = 0
        for i, individual in enumerate(sorted_population):
            cumulative_sum += (i + 1)
            if cumulative_sum >= R:
                return individual
        return sorted_population[-1]


    # Crossover Methods

    # not good for our problem since it can produce invalid sols ( contains duplications)
    def one_point_crossover(self, parent1: List['Landmark'], parent2: List['Landmark']):
        if min(len(parent1), len(parent2)) < 2:
            return parent1[:], parent2[:]
        point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    
    # the same problem as one-point-crossover
    def two_point_crossover(self, parent1: List['Landmark'], parent2: List['Landmark']):
        if min(len(parent1), len(parent2)) < 3:
            return parent1[:], parent2[:]
        point1 = random.randint(1, min(len(parent1), len(parent2)) - 2)
        point2 = random.randint(point1 + 1, min(len(parent1), len(parent2)) - 1)
        point1, point2 = min(point1, point2), max(point1, point2)
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        return child1, child2

    def pmx_crossover(self, parent1: List['Landmark'], parent2: List['Landmark']):
        if min(len(parent1), len(parent2)) < 2:
            return parent1[:], parent2[:]
        point1, point2 = sorted(random.sample(range(min(len(parent1), len(parent2))), 2))
        child1 = [None] * len(parent1)
        child2 = [None] * len(parent2)
        child1[point1:point2] = parent2[point1:point2]
        child2[point1:point2] = parent1[point1:point2]
        mapping1 = {parent2[i]: parent1[i] for i in range(point1, point2)}
        mapping2 = {parent1[i]: parent2[i] for i in range(point1, point2)}
        for i in range(len(parent1)):
            if i < point1 or i >=point2:
                gene = parent1[i]
                while gene in mapping1:
                    gene = mapping1[gene]
                child1[i] = gene

        for i in range(len(parent2)):
            if i < point1 or i >=point2:
                gene = parent2[i]
                while gene in mapping2:
                    gene = mapping2[gene]
                child2[i] = gene

        return child1, child2
    

    def order_crossover(self, parent1: List['Landmark'], parent2: List['Landmark']):
        limit = min(len(parent1), len(parent2))
        if limit < 2:
            return parent1[:], parent2[:]
        p1, p2 = sorted(random.sample(range(limit), 2))

        child1 = [None] * len(parent1)
        child1[p1:p2] = parent1[p1:p2]
        used1 = set(parent1[p1:p2])

        p2_idx = 0
        for i in range(len(child1)):
            if child1[i] is None:
                while p2_idx < len(parent2) and parent2[p2_idx] in used1:
                    p2_idx += 1
                if p2_idx < len(parent2):
                    child1[i] = parent2[p2_idx]
                    used1.add(parent2[p2_idx])
                    p2_idx += 1

        child1 = [g for g in child1 if g is not None]
        bigger1 = parent1 if len(parent1) > len(parent2) else parent2
        for gene in bigger1:
            if gene not in used1:
                child1.append(gene)
                used1.add(gene)

        child2 = [None] * len(parent2)
        child2[p1:p2] = parent2[p1:p2]
        used2 = set(parent2[p1:p2])

        p1_idx = 0
        for i in range(len(child2)):
            if child2[i] is None:
                while p1_idx < len(parent1) and parent1[p1_idx] in used2:
                    p1_idx += 1
                if p1_idx < len(parent1):
                    child2[i] = parent1[p1_idx]
                    used2.add(parent1[p1_idx])
                    p1_idx += 1

        child2 = [g for g in child2 if g is not None]
        bigger2 = parent1 if len(parent1) > len(parent2) else parent2
        for gene in bigger2:
            if gene not in used2:
                child2.append(gene)
                used2.add(gene)

        return child1, child2
    

    # unfortunately works only when the size of the parents is the same
    def cycle_crossover_for_permutations(self, parent1: List['Landmark'], parent2: List['Landmark']):
        cycle = []
        index = 0
        while index not in cycle:
            cycle.append(index)
            index = parent1.index(parent2[index])
        child1 = [None] * len(parent1)
        child2 = [None] * len(parent2)
        for i in range(len(parent1)):
            if i in cycle:
                child1[i] = parent1[i]
                child2[i] = parent2[i]
            else:
                child1[i] = parent2[i]
                child2[i] = parent1[i]
        return child1, child2

    def cycle_crossover(self, parent1: List['Landmark'], parent2: List['Landmark']):
        if not parent1 or not parent2:
            return parent1[:], parent2[:]

        common = set(parent1) & set(parent2)

        if len(common) < 2:
            return self.order_crossover(parent1, parent2)

        p1_common = [lm for lm in parent1 if lm in common]
        p2_common = [lm for lm in parent2 if lm in common]

        size = len(p1_common)
        visited = [False] * size
        cycles = []

        for start in range(size):
            if not visited[start]:
                cycle = []
                idx = start
                while not visited[idx]:
                    visited[idx] = True
                    cycle.append(idx)
                    idx = p1_common.index(p2_common[idx])
                cycles.append(cycle)

        child1_common = [None] * size
        child2_common = [None] * size

        for i, cycle in enumerate(cycles):
            for idx in cycle:
                if i % 2 == 0:
                    child1_common[idx] = p1_common[idx]
                    child2_common[idx] = p2_common[idx]
                else:
                    child1_common[idx] = p2_common[idx]
                    child2_common[idx] = p1_common[idx]

        p1_unique = [lm for lm in parent1 if lm not in common]
        p2_unique = [lm for lm in parent2 if lm not in common]
        all_unique = p1_unique + p2_unique
        random.shuffle(all_unique)

        half = len(all_unique) // 2
        child1 = child1_common + all_unique[:half + len(all_unique) % 2]
        child2 = child2_common + all_unique[half + len(all_unique) % 2:]

        return child1, child2
    

    # works for different size of parents
    def edge_recombination_crossover(self, parent1: List['Landmark'], parent2: List['Landmark'], neighborhood_selection: Literal['linear', 'circular'] = 'linear'):
            if not parent1 or not parent2:
                return (parent1 or [])[:], (parent2 or [])[:] 

            child_length = max(len(parent1), len(parent2))

            # Child 1 
            landmarks_mapping1 = self.erx_neighbor_map(parent1, parent2, neighborhood_selection)
            child1 = []
            current_landmark = parent1[0]

            while len(child1) < child_length:
                child1.append(current_landmark)

                for neighbors in landmarks_mapping1.values():
                    neighbors.discard(current_landmark)

                if len(child1) == child_length:
                    break

                if not landmarks_mapping1[current_landmark]:
                    remaining = list(landmarks_mapping1.keys() - set(child1))
                    if remaining:
                        current_landmark = random.choice(remaining)
                    else:
                        remaining_global = list(set(self.problem.landmarks) - set(child1))
                        current_landmark = random.choice(remaining_global)
                else:
                    neighbors_list = list(landmarks_mapping1[current_landmark])
                    min_size = min(len(landmarks_mapping1[n]) for n in neighbors_list)
                    candidates = [n for n in neighbors_list if len(landmarks_mapping1[n]) == min_size]
                    current_landmark = random.choice(candidates)

            # Child 2 
            landmarks_mapping2 = self.erx_neighbor_map(parent1, parent2, neighborhood_selection)
            child2 = []
            current_landmark = parent2[0]

            while len(child2) < child_length:
                child2.append(current_landmark)

                for neighbors in landmarks_mapping2.values():
                    neighbors.discard(current_landmark)

                if len(child2) == child_length:
                    break

                if not landmarks_mapping2[current_landmark]:
                    remaining = list(landmarks_mapping2.keys() - set(child2))
                    if remaining:
                        current_landmark = random.choice(remaining)
                    else:
                        remaining_global = list(set(self.problem.landmarks) - set(child2))
                        current_landmark = random.choice(remaining_global)
                else:
                    neighbors_list = list(landmarks_mapping2[current_landmark])
                    min_size = min(len(landmarks_mapping2[n]) for n in neighbors_list)
                    candidates = [n for n in neighbors_list if len(landmarks_mapping2[n]) == min_size]
                    current_landmark = random.choice(candidates)

            return child1, child2
    

        # i will add later more crossover methods for diffrent sizes

    # Mutation Methods

    def swap_mutation(self, individual: List['Landmark']):
        if len(individual) >= 2 and random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual


    def inversion_mutation(self, individual: List['Landmark']):
        if len(individual) >= 2 and random.random() < self.mutation_rate:
            idx1, idx2 = sorted(random.sample(range(len(individual)), 2))
            individual[idx1:idx2 + 1] = reversed(individual[idx1:idx2 + 1])
        return individual


    def scramble_mutation(self, individual: List['Landmark']):
        if len(individual) >= 2 and random.random() < self.mutation_rate:
            idx1, idx2 = sorted(random.sample(range(len(individual)), 2))
            subset = individual[idx1:idx2 + 1]
            random.shuffle(subset)
            individual[idx1:idx2 + 1] = subset
        return individual



    def insertion_mutation(self, individual: List['Landmark']):
        if random.random() < self.mutation_rate:
            available_landmarks = [loc for loc in self.problem.landmarks if individual and loc not in individual]
            if available_landmarks:
                added_landmark = random.choice(available_landmarks)
                insert_pos = random.randint(0, len(individual))
                individual.insert(insert_pos, added_landmark)
        return individual


    def deletion_mutation(self, individual: List['Landmark']):
        if len(individual) > 1 and random.random() < self.mutation_rate:
            delete_pos = random.randint(0, len(individual) - 1)
            individual.pop(delete_pos)
        return individual


    def displacement_mutation(self, individual: List['Landmark']):
        if len(individual) > 1 and random.random() < self.mutation_rate:
            idx1, idx2 = sorted(random.sample(range(len(individual)), 2))
            segment = individual[idx1:idx2 + 1]
            new_individual = individual[:idx1] + individual[idx2 + 1:]
            insert_pos = random.randint(0, len(new_individual))
            new_individual[insert_pos:insert_pos] = segment
            return new_individual
        return individual


    # The evolvement loop

    def evolve(self, selection_method, crossover_method, mutation_method,
           tournament_size=5, neighborhood_selection='linear', elitism_rate=0.1):
    
        self.population = sorted(self.population, key=self.calculate_fitness, reverse=True)
        best_overall = self.population[0]
        num_elitists = max(1, int(self.population_size * elitism_rate))
    

        for generation in range(self.generations):

            new_population = self.population[:num_elitists]
            
            max_attempts = self.population_size * 10  # ← guard against infinite loop
            attempts = 0
    
            while len(new_population) < self.population_size:
                attempts += 1
                if attempts > max_attempts:
                    
                    break
                
                if selection_method == 'tournament':
                    parent1 = self.tournament_selection(tournament_size)
                    parent2 = self.tournament_selection(tournament_size)
                elif selection_method == 'roulette':
                    parent1 = self.roulette_wheel_selection()
                    parent2 = self.roulette_wheel_selection()
                else:
                    parent1 = self.rank_selection()
                    parent2 = self.rank_selection()
    
                if crossover_method == 'one_point':
                    child1, child2 = self.one_point_crossover(parent1, parent2)
                elif crossover_method == 'two_point':
                    child1, child2 = self.two_point_crossover(parent1, parent2)
                elif crossover_method == 'pmx':
                    child1, child2 = self.pmx_crossover(parent1, parent2)
                elif crossover_method == 'order':
                    child1, child2 = self.order_crossover(parent1, parent2)
                elif crossover_method == 'cycle':
                    child1, child2 = self.cycle_crossover(parent1, parent2)
                else:
                    child1, child2 = self.edge_recombination_crossover(parent1, parent2, neighborhood_selection)
    
                if mutation_method == 'swap':
                    child1, child2 = self.swap_mutation(child1), self.swap_mutation(child2)
                elif mutation_method == 'inversion':
                    child1, child2 = self.inversion_mutation(child1), self.inversion_mutation(child2)
                elif mutation_method == 'scramble':
                    child1, child2 = self.scramble_mutation(child1), self.scramble_mutation(child2)
                elif mutation_method == 'insertion':
                    child1, child2 = self.insertion_mutation(child1), self.insertion_mutation(child2)
                elif mutation_method == 'deletion':
                    child1, child2 = self.deletion_mutation(child1), self.deletion_mutation(child2)
                else:
                    child1, child2 = self.displacement_mutation(child1), self.displacement_mutation(child2)

                child1 = self.repair_individual(child1)
                child2 = self.repair_individual(child2)


                if self.is_valid_individual(child1):
                    new_population.append(child1)
                if len(new_population) < self.population_size and self.is_valid_individual(child2):
                    new_population.append(child2)
    
            self.population = sorted(new_population[:self.population_size], key=self.calculate_fitness, reverse=True)
    
            if self.calculate_fitness(self.population[0]) > self.calculate_fitness(best_overall):
                best_overall = self.population[0][:]
    
        return best_overall



    # helper functions

    def calculate_total_distance(self, itinerary: List['Landmark']) -> float:
        total_distance = 0
        for i in range(len(itinerary) - 1):
            total_distance += self.problem.distance(itinerary[i], itinerary[i + 1])
        return total_distance
    

    def calculate_total_time(self, itinerary: List['Landmark']) -> float:
        if not itinerary:
            return 0

        total_time = self.problem.time_matrix[self.problem.hotel.id][itinerary[0].name]

        for i, landmark in enumerate(itinerary):
            total_time += landmark.visit_duration
            if i < len(itinerary) - 1:
                total_time += self.problem.time_matrix[landmark.name][itinerary[i + 1].name]

        total_time += self.problem.time_matrix[itinerary[-1].name][self.problem.hotel.id]

        return total_time / 60
    
    


    def erx_neighbor_map(self, parent1: List['Landmark'], parent2: List['Landmark'], neighborhood_selection: Literal['linear', 'circular' ] = 'linear'):
        unique_landmarks = set(parent1) | set(parent2)
        mapping = {landmark: set() for landmark in unique_landmarks}
        for parent in [parent1, parent2]:
            n = len(parent)
            for i, lm in enumerate(parent):
                if neighborhood_selection == 'circular':
                    if i > 0:
                        mapping[lm].add(parent[i - 1])
                    if i < n - 1:
                        mapping[lm].add(parent[i + 1])
                else:  
                    mapping[lm].add(parent[(i - 1) % n])
                    mapping[lm].add(parent[(i + 1) % n])
        return mapping


    def is_valid_individual(self, individual: List['Landmark']) -> bool:
        # if not individual:
        #     return False
        # if None in individual:
        #     return False
        # if len(set(lm.id for lm in individual)) != len(individual):
        #     return False
        # return True
        return self.problem.valid_state(individual, hard_constraints=True)
    

    def repair_individual(self, individual: List['Landmark']):
        if not individual:
            return individual
    
        # Remove None values and duplicates first
        seen_ids = set()
        cleaned = []
        for lm in individual:
            if lm is not None and lm.id not in seen_ids:
                cleaned.append(lm)
                seen_ids.add(lm.id)
    
        # Drop landmarks that violate the type filter (they can never be valid)
        if self.problem.type_filter:
            cleaned = [lm for lm in cleaned if lm.landmark_type in self.problem.type_filter]
    
        trip_start_time = 8.0  
        current_time = trip_start_time * 60  
        repaired = []
    
        for landmark in cleaned:
            if not repaired:
                travel_mins = self.problem.time_matrix[self.problem.hotel.id][landmark.name]
            else:
                travel_mins = self.problem.time_matrix[repaired[-1].name][landmark.name]
    
            arrival_time = current_time + travel_mins
    
            # If closed at arrival, try waiting until it opens
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
                
            if self.problem.type_filter and landmark.landmark_type not in self.problem.type_filter:
                continue
            
            return_mins = self.problem.time_matrix[landmark.name][self.problem.hotel.id]
            finish_time = arrival_time + landmark.visit_duration + return_mins
            if (finish_time / 60) - trip_start_time > self.problem.max_travel_time:
                continue
            
            repaired.append(landmark)
            current_time = arrival_time + landmark.visit_duration
    
        return repaired
    

    
# SMALL TESTING FOR DEBUGGIN :)

# landmarks = get_landmarks()
# hotels = get_hotels()
# time_matrix = get_time_matrix()

# selection_methods = [ 'tournament', 'roulette', 'rank']
# crossover_methods = [ 'one_point', 'two_point', 'pmx','order', 'cycle', 'edge_recombination']
# mutation_methods = ['insertion', 'deletion', 'displacement', 'swap', 'inversion', 'scramble']

# problem = TravelProblem_LocalSearch(landmarks, travel_information={ 'hotel': hotels[0], 'time_matrix': time_matrix, 'Travel_Time': 12, 'Travel_day': 'fri', 'type_filter': None, 'Landmarks_number': None })
# My_Algorithm = Genetic_Algorithm(problem, population_size=100, generations=100, mutation_rate=0.1)
# for selection in selection_methods:
#     for crossover in crossover_methods:
#         for mutation in mutation_methods:
#             random.seed(42)
#             My_Algorithm = Genetic_Algorithm(problem, population_size=100, generations=100, mutation_rate=0.1)
#             print(f"\nRunning GA with Selection: {selection}, Crossover: {crossover}, Mutation: {mutation}")
#             best_itinerary = My_Algorithm.evolve(selection_method=selection, crossover_method=crossover, mutation_method=mutation, tournament_size=5, neighborhood_selection='linear', elitism_rate=0.2)
#             print("Best Itinerary:", hotels[0], [landmark.name for landmark in best_itinerary], "\nTotal Interest Score:", sum(landmark.interest_score for landmark in best_itinerary), "\nTotal Time:", round(My_Algorithm.calculate_total_time(best_itinerary), 2), '\nNumber of Landmarks:', len(best_itinerary))
