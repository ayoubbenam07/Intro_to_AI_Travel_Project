from core.Node_Classes import Landmark
from typing import List

class Solution:

    def __init__(self, state:List[Landmark] , score :float):
        self.state = state
        self.score = score

    def present(self):

        s = []
        for landmark in self.state : 
            s.append(landmark.name)

        print(f"the solution list is \n {s} \n the score of the solution is {self.score}") 
        print(f"the length of result is {len(s)}")
