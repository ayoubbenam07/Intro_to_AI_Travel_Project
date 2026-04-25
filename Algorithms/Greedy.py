# impelemnt everything in details with docuementations and comments
from Intro_to_AI_Travel_Project.core.Problem_InformedSearch import (
    TravelProblem_InformedSearch,
)
from Intro_to_AI_Travel_Project.utils.data_loader import (
    get_landmarks,
    get_hotels,
    get_time_matrix,
)
from Intro_to_AI_Travel_Project.core.Node_Classes import Landmark, Hotel


def greedy_search(problem: TravelProblem_InformedSearch):
    state = problem.initial_state
    path = [state]

    while True:
        actions = problem.actions(state)

        if len(actions) == 1 and actions[0][0] == "return":
            final = problem.result(state, actions[0])
            return path + [final]

        best_action = min(
            actions, key=lambda a: problem.heuristic(state, problem.result(state, a))
        )

        state = problem.result(state, best_action)
        path.append(state)

    return None


# small test -_-

# landmarks = get_landmarks()
# hotels = get_hotels()
# time_matrix = get_time_matrix()

# my_problem = TravelProblem_InformedSearch(
#     hotels[0], landmarks, time_matrix, 720, 480, "fri"
# )
# path = greedy_search(my_problem)
# path_names = [(state[0], state[2]) for state in path]
# print(path_names)
