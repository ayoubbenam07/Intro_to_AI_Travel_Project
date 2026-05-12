"""
Greedy.py
=========
Implements **Greedy Best-First Search** for the Travel Guide planning problem.

Algorithm overview
------------------
Greedy Best-First Search always expands the action that leads to the state
with the *lowest heuristic value* h(n), completely ignoring the path cost
g(n).  It is fast but **not optimal** — it may miss a globally better route
in favour of locally attractive landmarks.

Search loop
-----------
1. From the current state, ask the problem for all legal actions.
2. If the only action is "return to hotel", append the final state and stop.
3. Otherwise, evaluate h(n) = heuristic(current, result(current, action))
   for every candidate action and greedily pick the minimum.
4. Transition to the chosen successor state and repeat.

Complexity
----------
- Time  : O(b · d)  where b = branching factor, d = solution depth.
- Space : O(d)      only the current path is kept in memory.
"""

from core.Problem_InformedSearch import TravelProblem_InformedSearch
from utils.data_loader import get_landmarks, get_hotels, get_time_matrix
from core.Node_Classes import Landmark, Hotel


def greedy_search(problem: TravelProblem_InformedSearch) -> list[tuple] | None:
    """
    Execute Greedy Best-First Search on a ``TravelProblem_InformedSearch`` instance.

    At each step the algorithm selects the successor whose *heuristic value* is
    the smallest (most promising), making a single irrevocable greedy choice
    without backtracking.

    The search terminates when the problem reports that the only available action
    is ``("return", hotel_name)``, meaning no more feasible landmarks exist within
    the remaining time budget.

    Parameters
    ----------
    problem : TravelProblem_InformedSearch
        A fully initialised problem instance containing:
        - ``problem.initial_state`` — starting state (hotel, empty visited set, start time).
        - ``problem.actions(state)`` — legal actions from a given state.
        - ``problem.result(state, action)`` — state reached after applying an action.
        - ``problem.heuristic(parent, child)`` — h(n) estimate for a state transition.

    Returns
    -------
    list[tuple] | None
        The ordered list of states visited along the greedy path, including the
        initial state and the terminal "return to hotel" state.
        Returns ``None`` only if the initial state itself is a dead-end with no
        actions — this should not occur in a well-formed problem.

    Notes
    -----
    - **No backtracking**: once a landmark is chosen it cannot be un-chosen.
    - **No visited deduplication** at the search level — the problem's action
      filter (via ``visited_landmarks`` in the state) prevents revisits.
    - The heuristic formula used by ``TravelProblem_InformedSearch`` is
      ``(travel_forward + travel_back) / interest_score``, which rewards
      nearby, high-interest landmarks.

    Examples
    --------
    >>> landmarks   = get_landmarks()
    >>> hotels      = get_hotels()
    >>> time_matrix = get_time_matrix()
    >>> problem = TravelProblem_InformedSearch(
    ...     hotels[0], landmarks, [], time_matrix,
    ...     time_budget=720, starting_time=480, visiting_day="mon"
    ... )
    >>> path = greedy_search(problem)
    >>> for position, visited, time in path:
    ...     print(f"{position:30s}  t={time} min")
    """
    # ── Initialisation ────────────────────────────────────────────────────────
    state = problem.initial_state  # (hotel_name, frozenset(), start_time)
    path = [state]  # keep the full sequence of states for inspection

    # ── Main search loop ──────────────────────────────────────────────────────
    while True:
        # 1. Expand: get all legal actions from the current state
        actions = problem.actions(state)

        # 2. Termination check: if the only action is to return, we are done
        if len(actions) == 1 and actions[0][0] == "return":
            # Compute the final "return to hotel" state and append it
            final = problem.result(state, actions[0])
            return path + [final]

        # 3. Greedy selection: pick the action whose resulting state has the
        #    lowest heuristic value h(current_state → successor_state).
        #
        #    Lambda breakdown:
        #      a                        → current candidate action tuple
        #      problem.result(state, a) → successor state if we take action a
        #      problem.heuristic(state, ...)
        #                               → h(n) of that successor (lower = better)
        best_action = min(
            actions,
            key=lambda a: problem.heuristic(state, problem.result(state, a)),
        )

        # 4. Transition: move to the chosen successor state (no backtracking)
        state = problem.result(state, best_action)
        path.append(state)

    # Unreachable — loop always exits via the return-action check above
    return None


# ── Quick smoke test ──────────────────────────────────────────────────────────
# Loads real data and runs one greedy search; prints the ordered route with
# arrival times.  Remove or guard with ``if __name__ == "__main__":`` in
# production code.

if __name__ == "__main__":
    landmarks = get_landmarks()
    hotels = get_hotels()
    time_matrix = get_time_matrix()

    my_problem = TravelProblem_InformedSearch(
        hotel=hotels[0],
        landmarks=landmarks,
        type_filter=[],  # no filter → consider all landmark types
        time_matrix=time_matrix,
        time_budget=720,  # 12-hour trip window (minutes)
        starting_time=480,  # trip starts at 08:00 (480 min from midnight)
        visiting_day="mon",
    )

    path = greedy_search(my_problem)

    # Extract (position_name, current_time) pairs for a readable summary
    path_names = [(state[0], state[2]) for state in path]
    print(path_names, len(path_names))
