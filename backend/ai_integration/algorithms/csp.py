"""
Constraint Satisfaction Problem Solver
========================================
"""

import time
from typing import List, Optional, Dict, Tuple
from ai_integration.core.node_classes import Landmark
from ai_integration.core.problems import TravelProblem_LocalSearch

SKIP = "__SKIP__"


class TravelCSP:
    """CSP formulation for travel planning"""
    
    def __init__(
        self,
        problem: TravelProblem_LocalSearch,
        inference_method: str = "fc",
        var_heuristic: str = "mrv",
        val_heuristic: str = "lcv",
        time_limit_s: float = 30.0
    ):
        self.problem = problem
        self.inference_method = inference_method
        self.var_heuristic = var_heuristic
        self.val_heuristic = val_heuristic
        self.time_limit_s = time_limit_s
        
        self.candidates = sorted(
            problem.landmarks,
            key=lambda lm: lm.interest_score,
            reverse=True
        )
        
        self.variables = list(range(len(self.candidates)))
        self.domains = {i: self.candidates + [SKIP] for i in self.variables}
        self.neighbors = {i: [j for j in self.variables if j != i] for i in self.variables}
        
        self.start_time = time.time()
        self._solution: Optional[Dict] = None
    
    def constraint(self, Xi: int, vi, Xj: int, vj) -> bool:
        """Check binary constraints"""
        # C1: AllDifferent
        if vi is not SKIP and vj is not SKIP and vi == vj:
            return False
        
        # C2: SKIP-last
        if abs(Xi - Xj) == 1:
            earlier_val = vi if Xi < Xj else vj
            later_val = vj if Xi < Xj else vi
            if earlier_val is SKIP and later_val is not SKIP:
                return False
        
        return True
    
    def nconflicts(self, var: int, val, assignment: Dict) -> int:
        """Count conflicts"""
        conflicts = 0
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if not self.constraint(var, val, neighbor, assignment[neighbor]):
                    conflicts += 1
        return conflicts
    
    def forward_check(self, var: int, val, assignment: Dict) -> bool:
        """Simple forward checking"""
        for neighbor in self.neighbors[var]:
            if neighbor not in assignment:
                for v in self.domains[neighbor]:
                    if not self.constraint(var, val, neighbor, v):
                        self.domains[neighbor].remove(v)
                        if not self.domains[neighbor]:
                            return False
        return True
    
    def backtrack(self, assignment: Dict) -> Optional[Dict]:
        """Backtracking search"""
        if time.time() - self.start_time > self.time_limit_s:
            return None
        
        if len(assignment) == len(self.variables):
            return assignment
        
        # Select unassigned variable
        if self.var_heuristic == "mrv":
            var = min(
                (v for v in self.variables if v not in assignment),
                key=lambda v: len(self.domains[v]),
                default=None
            )
        else:
            var = next((v for v in self.variables if v not in assignment), None)
        
        if var is None:
            return None
        
        # Try each value
        for val in self.domains[var]:
            if self.nconflicts(var, val, assignment) == 0:
                assignment[var] = val
                
                if self.forward_check(var, val, assignment):
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                
                del assignment[var]
        
        return None
    
    def solve(self) -> List[Landmark]:
        """Solve CSP and return path"""
        assignment = self.backtrack({})
        
        if not assignment:
            return self.problem.initial_state
        
        result = []
        for i in sorted(assignment.keys()):
            if assignment[i] is not SKIP:
                result.append(assignment[i])
        
        return result if self.problem.valid_state(result) else self.problem.initial_state
