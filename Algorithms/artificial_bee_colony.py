"""
artificial_bee_colony.py
========================
Implements the **Artificial Bee Colony (ABC)** metaheuristic for the
Travel Guide optimisation problem.

Algorithm overview
------------------
ABC mimics the foraging behaviour of a honey-bee swarm.  The colony is
divided into three functional groups:

1. **Employed bees** (one per food source / solution):
   Each employed bee exploits its assigned food source by generating a
   neighbour solution.  If the neighbour is better, the bee moves to it;
   otherwise a ``limit`` counter is incremented.

2. **Onlooker bees** (remaining colony members):
   Onlooker bees observe the employed bees' "waggle dances" (fitness
   values) and probabilistically choose a food source to exploit further.
   Better sources attract more onlookers (selection pressure).

3. **Scout bees** (triggered by abandonment):
   When an employed bee's ``limit`` counter exceeds the threshold, its
   food source is considered exhausted.  The bee becomes a *scout* and
   randomly generates a brand-new solution, maintaining population diversity
   and preventing premature convergence.

Optimisation direction
----------------------
**Maximisation** — higher fitness is better.
``problem.evaluate(state)`` must return a non-negative float.

References
----------
- Karaboga, D. (2005). *An idea based on honey bee swarm for numerical
  optimization.* Technical Report TR06, Erciyes University.
"""

from core.Problem_LocalSearch import TravelProblem_LocalSearch
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Node_Classes import Landmark, Hotel
import math
import random


# ──────────────────────────────────────────────────────────────────────────────
# Data class
# ──────────────────────────────────────────────────────────────────────────────

class Bee:
    """
    Represents a single employed bee (i.e. one candidate solution / food source).

    Attributes
    ----------
    fitness : float
        Quality score of the current solution.  Higher is better (maximisation).
    state : list[Landmark]
        The ordered itinerary (sequence of landmarks) this bee currently holds.
    limit : int
        Abandonment counter.  Incremented each iteration the bee fails to
        improve its solution.  When ``limit >= ABC_Optimization.limit`` the
        food source is abandoned and the bee becomes a scout.
    """

    def __init__(self, fitness: float, state: list[Landmark]):
        """
        Parameters
        ----------
        fitness : float
            Initial fitness of the solution.
        state : list[Landmark]
            Initial ordered itinerary assigned to this bee.
        """
        self.fitness = fitness
        self.state   = state
        self.limit   = 0   # no failed attempts yet


# ──────────────────────────────────────────────────────────────────────────────
# Main optimiser
# ──────────────────────────────────────────────────────────────────────────────

class ABC_Optimization:
    """
    Artificial Bee Colony optimiser for the Travel Guide problem.

    The colony is split into *employed bees* and *onlooker bees* according to
    ``colony_ratio``.  Each call to ``solve()`` runs the three-phase loop
    (employed → onlooker → scout) for ``iterations`` cycles and returns the
    best solution found globally.

    Attributes
    ----------
    problem : TravelProblem_LocalSearch
        The problem instance providing state generation, neighbour generation,
        and fitness evaluation.
    colony_size : int
        Total number of bees (employed + onlooker).
    colony_ratio : float
        Fraction of the colony that are employed bees (range 0 < r < 1).
    limit : int
        Maximum number of non-improving iterations before a food source is
        abandoned and the bee becomes a scout.
    iterations : int
        Number of full ABC cycles to run.  Defaults to ``math.inf`` (run
        forever — caller is expected to provide a finite value in practice).
    selection_method : str
        Strategy used by onlooker bees to choose which food source to exploit.
        One of ``"roulette"``, ``"tournament"``, or ``"rank"``.
    employed_bee_number : int
        Computed as ``ceil(colony_size * colony_ratio)``.
    onlooker_bee_number : int
        Computed as ``colony_size - employed_bee_number``.
    global_best_state : list[Landmark] | None
        The best itinerary found across all iterations and all bees.
    global_best_fitness : float
        Fitness of ``global_best_state``.
    population : list[Bee]
        The current set of employed bees (food sources).
    """

    def __init__(
        self,
        problem: TravelProblem_LocalSearch,
        colony_ratio: float = 0.5,
        colony_size: int = 50,
        limit: int = 20,
        iterations: int = math.inf,
        selection_method: str = "roulette",
    ):
        """
        Initialise the ABC optimiser and seed the initial population.

        Parameters
        ----------
        problem : TravelProblem_LocalSearch
            Fully configured problem instance.  Must expose:
            - ``_generate_random_state()``        → random valid itinerary
            - ``_generate_random_neighbor_fast(state)`` → mutated neighbour
            - ``evaluate(state)``                 → fitness (float, higher = better)
        colony_ratio : float, optional
            Fraction of bees that are *employed* (default 0.5).
            The remaining (1 - colony_ratio) fraction are *onlooker* bees.
            Valid range: (0, 1).  A ratio of 0.5 gives equal halves.
        colony_size : int, optional
            Total number of bees in the swarm (default 50).
            Larger colonies explore more of the search space per iteration
            but increase per-iteration compute cost.
        limit : int, optional
            Abandonment threshold (default 20).  If an employed bee fails to
            improve its solution for ``limit`` consecutive iterations it abandons
            the food source and scouts a random new one.
            Lower values → more exploration (quicker abandonment).
            Higher values → more exploitation (persist longer on a source).
        iterations : int, optional
            Number of complete ABC cycles (employed → onlooker → scout) to
            execute before returning (default ``math.inf``).
            Always supply a finite integer for practical use.
        selection_method : str, optional
            Onlooker bee selection strategy (default ``"roulette"``).
            - ``"roulette"``   : fitness-proportionate selection (higher fitness
                                 → proportionally higher probability of being chosen).
            - ``"tournament"`` : random tournament of 3 bees; best wins.
            - ``"rank"``       : rank-based selection (best-ranked bee has highest
                                 chance; mitigates dominance of very high-fitness bees).
        """
        self.problem          = problem
        self.colony_size      = colony_size
        self.colony_ratio     = colony_ratio
        self.limit            = limit
        self.iterations       = iterations
        self.selection_method = selection_method

        # Derive employed / onlooker split from ratio
        self.employed_bee_number  = math.ceil(self.colony_size * self.colony_ratio)
        self.onlooker_bee_number  = self.colony_size - self.employed_bee_number
        print("eb : ", self.employed_bee_number, "ob : ", self.onlooker_bee_number)

        # Global best bookkeeping
        self.global_best_state   = None
        self.global_best_fitness = -1        # sentinel for "no solution yet"
        self.population          = []

        # ── Seed the employed bee population ──────────────────────────────────
        # Each employed bee starts on a random food source (random valid itinerary).
        for _ in range(self.employed_bee_number):
            random_state = self.problem._generate_random_state()
            fitness      = self.problem.evaluate(random_state)
            self.population.append(Bee(fitness, random_state))

        # Initialise global best from the seeded population
        if self.population:
            best_initial_bee         = max(self.population, key=lambda bee: bee.fitness)
            self.global_best_fitness = best_initial_bee.fitness
            self.global_best_state   = best_initial_bee.state[:]  # defensive copy

    # ──────────────────────────────────────────────────────────────────────────
    # Fitness helper
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_fitness(self, state: list[Landmark]) -> float:
        """
        Delegate fitness evaluation to the problem instance.

        Parameters
        ----------
        state : list[Landmark]
            An itinerary to score.

        Returns
        -------
        float
            Fitness value; higher is better (maximisation problem).
        """
        return self.problem.evaluate(state)

    # ──────────────────────────────────────────────────────────────────────────
    # Selection strategies
    # ──────────────────────────────────────────────────────────────────────────

    def tournament_selection(self, tournament_size: int = 3) -> Bee:
        """
        Select a bee via **tournament selection**.

        Randomly sample ``tournament_size`` bees from the population and return
        the one with the highest fitness.  Larger tournaments apply stronger
        selection pressure (best solution wins more often).

        Parameters
        ----------
        tournament_size : int, optional
            Number of bees participating in each tournament (default 3).

        Returns
        -------
        Bee
            The winning (highest-fitness) bee from the sampled tournament.
        """
        tournament_players = random.sample(self.population, tournament_size)
        winner = max(tournament_players, key=lambda player: player.fitness)
        return winner

    def roulette_wheel_selection(self) -> Bee:
        """
        Select a bee via **fitness-proportionate (roulette-wheel) selection**.

        Each bee's probability of being chosen is proportional to its fitness
        relative to the total population fitness.  Bees with higher fitness
        are selected more often, but every bee has a non-zero chance.

        Negative fitness values are handled by shifting all weights to be
        positive before computing probabilities (adds ``|min_fitness| + ε``).

        Returns
        -------
        Bee
            The selected bee.
        """
        fitnesses   = [bee.fitness for bee in self.population]
        min_fitness = min(fitnesses)

        # Shift weights so all are strictly positive (required by random.choices)
        if min_fitness < 0:
            weights = [f - min_fitness + 1e-6 for f in fitnesses]
        else:
            weights = [f + 1e-6 for f in fitnesses]  # ε prevents zero-weight

        winner = random.choices(self.population, weights=weights, k=1)[0]
        return winner

    def rank_selection(self) -> Bee:
        """
        Select a bee via **rank-based selection**.

        Bees are sorted by fitness (ascending) and assigned integer ranks
        1, 2, …, N.  Selection probability is proportional to rank rather than
        raw fitness, which reduces the dominance of extremely high-fitness
        individuals and maintains diversity.

        Returns
        -------
        Bee
            The selected bee (higher-ranked bees are more likely to be picked).
        """
        # Sort ascending so the best bee gets the highest rank (N)
        sorted_bees = sorted(self.population, key=lambda bee: bee.fitness)
        ranks       = list(range(1, len(self.population) + 1))
        winner      = random.choices(sorted_bees, weights=ranks, k=1)[0]
        return winner

    # ──────────────────────────────────────────────────────────────────────────
    # ABC phases
    # ──────────────────────────────────────────────────────────────────────────

    def _employed_bee_phase_(self):
        """
        **Phase 1 — Employed Bee Phase** (exploitation of known food sources).

        Each employed bee generates one neighbouring solution by applying a
        fast random perturbation to its current state.  If the neighbour
        is better, the bee moves to it and resets its abandonment counter.
        Otherwise, the counter is incremented toward the abandonment threshold.

        Global best is updated whenever a new best solution is discovered.

        Complexity: O(employed_bee_number × neighbour_generation_cost)
        """
        for bee in self.population:
            # Generate a random neighbour of the bee's current food source
            new_state   = self.problem._generate_random_neighbor_fast(bee.state)
            new_fitness = self.calculate_fitness(new_state)

            if new_fitness > bee.fitness:
                # Improvement found → move to the new source and reset counter
                bee.state   = new_state
                bee.fitness = new_fitness
                bee.limit   = 0

                # Check if this is a new global best
                if new_fitness > self.global_best_fitness:
                    self.global_best_fitness = new_fitness
                    self.global_best_state   = new_state[:]  # defensive copy

            else:
                # No improvement → increment abandonment counter
                bee.limit += 1

    def _onlooker_bee_phase_(self):
        """
        **Phase 2 — Onlooker Bee Phase** (fitness-guided exploitation).

        Onlooker bees watch the "dances" of employed bees (fitness signals)
        and choose a food source to exploit, biased toward better sources.
        Each onlooker then independently generates a neighbour of the chosen
        source and applies the same greedy-acceptance criterion.

        The selection strategy is controlled by ``self.selection_method``:
        - ``"roulette"``   → ``roulette_wheel_selection()``
        - ``"tournament"`` → ``tournament_selection(3)``
        - ``"rank"``       → ``rank_selection()``
        - anything else   → falls back to tournament (defensive default)

        Complexity: O(onlooker_bee_number × neighbour_generation_cost)
        """
        for _ in range(self.onlooker_bee_number):
            # Select a target food source (employed bee) based on fitness
            match self.selection_method:
                case "tournament":
                    target_bee = self.tournament_selection(3)
                case "roulette":
                    target_bee = self.roulette_wheel_selection()
                case "rank":
                    target_bee = self.rank_selection()
                case _:
                    # Defensive fallback for unrecognised method strings
                    target_bee = self.tournament_selection(3)

            # Explore a neighbourhood of the selected food source
            new_state   = self.problem._generate_random_neighbor_fast(target_bee.state)
            new_fitness = self.calculate_fitness(new_state)

            if new_fitness > target_bee.fitness:
                # Improvement → update the target bee's food source
                target_bee.state   = new_state
                target_bee.fitness = new_fitness
                target_bee.limit   = 0

                # Update global best if needed
                if new_fitness > self.global_best_fitness:
                    self.global_best_fitness = new_fitness
                    self.global_best_state   = new_state[:]

            else:
                target_bee.limit += 1

    def _scout_bee_phase_(self):
        """
        **Phase 3 — Scout Bee Phase** (diversity / exploration).

        Any employed bee whose abandonment counter (``bee.limit``) has reached
        or exceeded the ``self.limit`` threshold is considered to have exhausted
        its food source.  It becomes a *scout*, discards the old solution, and
        randomly generates a completely new one.

        This mechanism prevents the algorithm from stagnating around a local
        optimum by injecting fresh random solutions into the population.

        Note: the scout's new solution always replaces the old one regardless
        of quality — the bet is that a random jump will eventually land in a
        better basin of attraction.
        """
        for bee in self.population:
            if bee.limit >= self.limit:
                # Abandon current food source and scout a random new one
                new_state   = self.problem._generate_random_state()
                new_fitness = self.calculate_fitness(new_state)

                bee.state   = new_state
                bee.fitness = new_fitness
                bee.limit   = 0   # reset counter for the new food source

                # Still track global best in case the scout lands somewhere great
                if new_fitness > self.global_best_fitness:
                    self.global_best_fitness = new_fitness
                    self.global_best_state   = new_state[:]

    # ──────────────────────────────────────────────────────────────────────────
    # Entry point
    # ──────────────────────────────────────────────────────────────────────────

    def solve(self) -> tuple[list[Landmark], float]:
        """
        Run the full ABC optimisation loop for ``self.iterations`` cycles.

        Each cycle executes the three phases in order:
        1. :py:meth:`_employed_bee_phase_`  — exploit known sources
        2. :py:meth:`_onlooker_bee_phase_`  — guided exploitation of better sources
        3. :py:meth:`_scout_bee_phase_`     — abandon exhausted sources, explore randomly

        Returns
        -------
        tuple[list[Landmark], float]
            A 2-tuple of:
            - ``global_best_state``   : the best itinerary (ordered landmark list) found.
            - ``global_best_fitness`` : its fitness score (higher is better).

        Example
        -------
        >>> abc = ABC_Optimization(problem, colony_size=40, iterations=100)
        >>> best_route, best_score = abc.solve()
        >>> print("Score:", best_score)
        >>> print("Route:", [l.name for l in best_route])
        """
        current_iteration = 0

        while current_iteration < self.iterations:
            self._employed_bee_phase_()   # Phase 1: exploitation by employed bees
            self._onlooker_bee_phase_()   # Phase 2: guided exploitation by onlookers
            self._scout_bee_phase_()      # Phase 3: random exploration by scouts
            current_iteration += 1

        return self.global_best_state, self.global_best_fitness

    def calculate_total_time(self, itinerary: list[Landmark]) -> float:
        """
        Calculate the total duration of a given itinerary in hours.
        Includes travel from hotel to first landmark, all visits,
        travel between landmarks, and travel back to the hotel.
        """
        if not itinerary:
            return 0

        # Travel from hotel to first landmark
        total_time = self.problem.time_matrix[self.problem.hotel.id][itinerary[0].name]

        for i, landmark in enumerate(itinerary):
            # Time spent visiting the landmark
            total_time += landmark.visit_duration
            
            # Travel to the next landmark
            if i < len(itinerary) - 1:
                total_time += self.problem.time_matrix[landmark.name][itinerary[i + 1].name]

        # Travel back to the hotel from the final landmark
        total_time += self.problem.time_matrix[itinerary[-1].name][self.problem.hotel.id]

        return total_time / 60  # convert minutes to hours