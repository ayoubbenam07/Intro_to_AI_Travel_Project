"""
Greedy Best-First Search Algorithm
====================================
"""

from typing import List, Tuple, Optional
from ai_integration.core.node_classes import Landmark
from ai_integration.core.problems import TravelProblem_InformedSearch


def greedy_search(problem: TravelProblem_InformedSearch) -> List[Landmark]:
    """
    Greedy Best-First Search for travel planning.
    Always picks the landmark with the lowest heuristic value.
    """
    state = problem.initial_state
    path = []
    
    while True:
        actions = problem.actions(state)
        
        # Termination: only return action available
        if len(actions) == 1 and actions[0][0] == "return":
            break
        
        # Greedy selection: pick lowest heuristic
        best_action = min(
            actions,
            key=lambda a: problem.heuristic(state, problem.result(state, a))
        )
        
        state = problem.result(state, best_action)
        
        # Extract landmark name if it's a visit action
        if best_action[0] == "visit":
            landmark = problem.get_landmark_by_name(best_action[1])
            if landmark:
                path.append(landmark)
    
    return path
