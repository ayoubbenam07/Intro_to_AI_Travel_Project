from core.Node_Classes import Landmark

def calculate_unified_score(path, time_matrix):
    """Evaluation function for All algorithms 
        
        paramters : 
            path : the full path from hotel to state back to hotel : HOTEL + STATE + HOTEL
            time_matrix : the time matrix that we use from data_loader.py

        Output : 
            float number , score of the path    
    """
    if not path: return 0
    total_rating = sum(node.interest_score for node in path if isinstance(node, Landmark))
    total_travel_time = sum(time_matrix[path[i].name][path[i+1].name] for i in range(len(path) - 1))
    return (7 * total_rating) - total_travel_time
