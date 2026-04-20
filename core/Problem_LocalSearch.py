import random
import math

class TravelProblem_LocalSearch:

    """This class represent the travel guide problem formulation and its functions"""

    def __init__(self , landmarks:list[Landmark] , Travel_information:dict):

        #Travel_information dict should contains :  starting_coordinates: set[int ,int] ,Travel_day:str ,Travel_Time:float , Landmarks_number:int , type_filter:list[str]

        if not landmarks:
            raise ValueError("not list of landmarks provided ! ")
        
        self.landmarks = landmarks

        self.landmarks_list = list(landmarks.name)
        self.intial_state = self._generate_randome_state()

        # the user select it from the list of hotels
        self.hotel = Travel_information[hotel]
        self.Travel_day = Travel_information[Travel_day]
        
        # the user enters it as input 
        self.max_travel_time = Travel_information[Travel_Time]

        # maximum number of landmarks to visit , the user enter it 
        self.Landmarks_number = Travel_information[Landmarks_number]

        # filtering the type of landmarks the user want to visit
        self.type_filter = Travel_information[type_filter]


     

    def valid_state(self ,state:list[int])->bool:

        """Validate a special state based on opening and closing hours and type filtering """

        # the starting visiting hour , we can make it as input
        starting_hour = 8
        
        for i,landmark in enumerate(state):
            
            if not landmark : return False

            # if(starting_hour == 8 ): 

                        #  starting_hour += time_matrix[hotel.id][landmark.name] 
            #  else :

                        #  starting_hour += time_matrix[state[i-1].name][landmark.name]

    
           
            if not landmark.is_open(self.Travel_day , starting_hour ): return False

            if not self.landmark.landmark_type in self.type_filter : return False

            starting_hour += landmark.visit_duration /60

            
        return True 



    def _generate_randome_state(self):
        """generate random state to start with , without including the hotel"""    

        state = [ None for _ in range(self.Landmarks_number)]

        while not self.valid_state(state):

            state = [ random.choice(self.landmarks) for _ in range(self.Landmarks_number)] 

        return state
    


    def generate_neighbors(self,state):

        neighbors = []
        for landmark in state :
            for item in self.landmarks




    

    def _generate_random_neighbor(self , state:list[Landmark]):

        return None


    #evaluate a state based on : total distance , total rating , respecting the other constrains
    def evaluate(self , state)->float:

        return None
    

    def distance(self , landmark1 , landmark2):

        x = math.abs(landmark1.lat - landmark2.lat)
        y = math.abs(landmark1.lon - landmark2.log)

        return math.sqrt(x**2 + y**2)
        
        


