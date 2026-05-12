"""
Problem_InformedSearch.py
=========================
Defines the travel-planning problem in the **Informed Search** (heuristic-driven)
paradigm.  The state space is explored by algorithms such as Greedy Best-First or
A* that need both a *result* function and a *heuristic* function.

Problem formulation
-------------------
- **State**  : (current_position: str, visited_landmarks: frozenset[str], current_time: int)
- **Initial** : (hotel.name, frozenset(), starting_time)
- **Actions** : visit any unvisited, open, reachable landmark — or return to hotel
- **Goal**   : implicit; search ends when the only legal action is "return"
- **Cost**   : total elapsed time since departure (used by cost-sensitive algorithms)
- **Heuristic**: (travel_forward + travel_back) / interest_score  — favours nearby,
                 high-value landmarks; lower value ⟹ better candidate
"""

from core.Node_Classes import Landmark, Hotel


class TravelProblem_InformedSearch:
    """
    Formal problem definition for the Travel Guide planning task, tailored for
    **informed (heuristic) search** algorithms (Greedy Best-First, A*, etc.).

    The agent starts at a hotel, visits as many landmarks as possible within a
    fixed time budget, and must return to the hotel before the budget expires.
    Every landmark must be open on the visiting day at the moment of arrival.

    Attributes
    ----------
    hotel : Hotel
        The departure/return base for the trip.
    landmarks : list[Landmark]
        The candidate landmarks after applying the optional type filter.
    landmark_map : dict[str, Landmark]
        Fast name → Landmark lookup table built from the *unfiltered* landmark list.
    time_matrix : dict[str, dict[str, float]]
        Nested dict mapping (origin_name → destination_name → travel_time_minutes).
    time_budget : int
        Maximum trip duration in minutes (e.g. 720 for a 12-hour day).
    starting_time : int
        Absolute start time in minutes from midnight (e.g. 480 = 08:00).
    end_time : int
        Computed deadline = starting_time + time_budget.
    visiting_day : str
        Day of the week string used to check landmark opening hours (e.g. "mon").
    initial_state : tuple
        The search start state: (hotel.name, frozenset(), starting_time).
    """

    def __init__(
        self,
        hotel: Hotel,
        landmarks: list[Landmark],
        type_filter: list[str],
        time_matrix: dict[str, dict[str, float]],
        time_budget: int,
        starting_time: int,
        visiting_day: str,
    ):
        """
        Initialise the informed-search problem.

        Parameters
        ----------
        hotel : Hotel
            Starting and ending location for the tour.
        landmarks : list[Landmark]
            Full list of candidate landmarks loaded from the data source.
        type_filter : list[str]
            Optional whitelist of landmark types (e.g. ["museum", "park"]).
            Pass an empty list ``[]`` to include every landmark regardless of type.
        time_matrix : dict[str, dict[str, float]]
            Pairwise travel-time matrix keyed by location names.
            Access pattern: ``time_matrix[origin][destination]`` → minutes.
        time_budget : int
            Total available time for the trip in **minutes**.
        starting_time : int
            Trip start time expressed as minutes from midnight.
            Example: 480 = 08:00, 720 = 12:00.
        visiting_day : str
            Short lowercase day string used to query ``Landmark.is_open()``.
            Example: "mon", "tue", … "sun".
        """
        self.hotel = hotel

        # ── Type filtering ────────────────────────────────────────────────────
        # If a filter list is provided, keep only landmarks whose type matches.
        # Comparison is case-insensitive to tolerate mixed-case data.
        if len(type_filter) > 0:
            lower_filter = [t.lower() for t in type_filter]
            self.landmarks = [
                landmark
                for landmark in landmarks
                if landmark.landmark_type.lower() in lower_filter
            ]
        else:
            # No filter → every landmark is a candidate
            self.landmarks = landmarks

        # Build a fast O(1) lookup dict from the FULL (unfiltered) landmark list
        # so that result() and heuristic() can resolve names regardless of filtering.
        self.landmark_map = {l.name: l for l in landmarks}

        self.time_matrix = time_matrix
        self.time_budget = time_budget
        self.starting_time = starting_time
        self.end_time = starting_time + time_budget  # hard deadline
        self.visiting_day = visiting_day

        # ── Initial state ─────────────────────────────────────────────────────
        # Tuple layout: (current_position, visited_set, current_time)
        #   - current_position : name of the location the agent is currently at
        #   - visited_set      : frozenset of visited landmark *names*
        #   - current_time     : minutes elapsed from midnight at the current moment
        self.initial_state = (
            self.hotel.name,  # agent starts at the hotel
            frozenset(),  # no landmarks visited yet
            self.starting_time,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Helper
    # ──────────────────────────────────────────────────────────────────────────

    def get_landmark_by_name(self, name: str) -> Landmark | None:
        """
        Retrieve a Landmark object by its unique name.

        Parameters
        ----------
        name : str
            The landmark's name exactly as stored in ``landmark_map``.

        Returns
        -------
        Landmark | None
            The matching Landmark, or ``None`` if the name is not found.
        """
        return self.landmark_map.get(name)

    # ──────────────────────────────────────────────────────────────────────────
    # Core problem interface
    # ──────────────────────────────────────────────────────────────────────────

    def actions(self, state: tuple) -> list[tuple[str, str]]:
        """
        Return the list of legal actions available from ``state``.

        An action is a 2-tuple ``(action_type, location_name)``:
        - ``("visit", landmark_name)`` — travel to and visit the landmark.
        - ``("return", hotel_name)``   — go back to the hotel (trip ends).

        A landmark is a legal visit target only if **all** of the following hold:
        1. It has not already been visited in this trip.
        2. The agent can travel there and arrive while the landmark is open.
        3. After visiting, there is still enough time to travel back to the hotel
           before ``end_time``.

        If no landmark satisfies all three conditions the only legal action is
        to return to the hotel.

        Parameters
        ----------
        state : tuple
            Current search state ``(current_position, visited_landmarks, current_time)``.

        Returns
        -------
        list[tuple[str, str]]
            A list of ``(action_type, location_name)`` pairs.
            Always contains at least ``[("return", hotel_name)]``.
        """
        current_position, visited_landmarks, current_time = state
        possible_actions = []

        for landmark in self.landmarks:
            # Skip already-visited landmarks
            if landmark.name in visited_landmarks:
                continue

            # ── Feasibility check ─────────────────────────────────────────────
            # Time to travel from current position to the candidate landmark
            travel_forward = self.time_matrix[current_position][landmark.name]
            arrival_time = current_time + travel_forward

            # Time to travel from the landmark back to the hotel
            travel_back = self.time_matrix[landmark.name][self.hotel.name]
            # Earliest possible return time if we visit this landmark
            return_time = arrival_time + travel_back + landmark.visit_duration

            # Some landmarks may not have opening hours for every day (e.g. missing 'sun').
            # Treat a missing day as "closed" rather than crashing.
            try:
                is_open = landmark.is_open(self.visiting_day, arrival_time)
            except KeyError:
                is_open = False

            if is_open and return_time <= self.end_time:
                possible_actions.append(("visit", landmark.name))

        # If no landmark is reachable / feasible, force a return to hotel
        if not possible_actions:
            possible_actions.append(("return", self.hotel.name))

        return possible_actions

    def result(self, state: tuple, action: tuple[str, str]) -> tuple:
        """
        Apply ``action`` to ``state`` and return the resulting new state.

        Time accounting:
        - For a "visit" action the clock advances by (travel_time + visit_duration).
        - For a "return" action only travel_time is added (no visit_duration at hotel).

        Parameters
        ----------
        state : tuple
            Current state ``(current_position, visited_landmarks, current_time)``.
        action : tuple[str, str]
            Action to apply, e.g. ``("visit", "Casbah")`` or ``("return", "Hotel Sofitel")``.

        Returns
        -------
        tuple
            New state ``(next_position, new_visited_landmarks, new_current_time)``.
        """
        current_position, visited_landmarks, current_time = state
        travel_type, next_position = action

        # Travel time from current position to the next one
        travel_forward = self.time_matrix[current_position][next_position]

        # Start with the existing visited set; we may extend it below
        new_visited_landmarks = visited_landmarks
        visit_duration = 0

        if travel_type == "visit":
            # Add the visited landmark to the frozen set (creates a new frozenset)
            new_visited_landmarks = visited_landmarks | frozenset([next_position])
            # Fetch the visit duration from the landmark object
            landmark = self.get_landmark_by_name(next_position)
            visit_duration = landmark.visit_duration

        # Advance the clock
        new_current_time = current_time + travel_forward + visit_duration

        return (next_position, new_visited_landmarks, new_current_time)

    def heuristic(self, parent_state: tuple, child_state: tuple) -> float:
        """
        Estimate the "cost" (lower is better) of moving from ``parent_state``
        to ``child_state``.

        Formula
        -------
        ``h = (travel_forward + travel_back) / interest_score``

        Intuition:
        - Numerator   : round-trip travel cost (time) for visiting the child landmark.
        - Denominator : how interesting the landmark is (higher score → cheaper).

        This biases the search towards **high-value, nearby** landmarks and is
        admissible in the sense that it captures both distance and quality.

        Special case: if ``child_state`` is the hotel (return action), ``h = 0``
        because no further exploration is possible.

        Parameters
        ----------
        parent_state : tuple
            The state from which the move originates
            ``(parent_position, visited, time)``.
        child_state : tuple
            The state reached after the action
            ``(child_position, visited, time)``.

        Returns
        -------
        float
            Heuristic cost estimate. Lower values are preferred by Greedy / A*.
        """
        parent_position, _, _ = parent_state
        child_position, _, _ = child_state

        # Returning to hotel has no further exploration value
        if child_position == self.hotel.name:
            return 0

        travel_forward = self.time_matrix[parent_position][child_position]
        travel_back = self.time_matrix[child_position][self.hotel.name]

        landmark = self.get_landmark_by_name(child_position)
        landmark_score = landmark.interest_score

        # Avoid division by zero for degenerate data
        return (travel_forward + travel_back) / landmark_score

    def path_cost(self, state: tuple) -> int:
        """
        Return the cumulative cost of reaching ``state`` from the initial state.

        Cost is defined as **total minutes elapsed** since the trip started.
        This is used by cost-sensitive algorithms (e.g. A*) as ``g(n)``.

        Parameters
        ----------
        state : tuple
            Any search state ``(position, visited, current_time)``.

        Returns
        -------
        int
            Minutes elapsed since ``starting_time``.
        """
        _, _, current_time = state
        return current_time - self.starting_time
