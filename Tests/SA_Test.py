import sys
import os

# Get the directory of the current file (Tests), then go up one level to the root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


from Algorithms.Simulated_Anealing import Simulated_Annealing
from core.Problem_LocalSearch import TravelProblem_LocalSearch
from core.Solution import Solution
from utils import data_loader
import random

landmarks = data_loader.get_landmarks()


hotels =  data_loader.get_hotels()


time_matrix = data_loader.get_time_matrix()

days = ["mon","tue", "wed" ,"thu","fri","sat","sun"]

           
travel_information = {
    "hotel": random.choice(hotels),
    "Travel_day" : random.choice(days),
    "Travel_Time": 10 ,
    "type_filter" : None  ,
    "time_matrix": time_matrix,
    "trip_start_time" : 8
}

problem = TravelProblem_LocalSearch(landmarks ,travel_information)



sa = Simulated_Annealing(problem)


result = sa.run()

solution = Solution( result , sa.calculate_fitness(result))

solution.present()
 


