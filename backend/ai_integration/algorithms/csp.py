from __future__ import annotations

import sys
import os
import time
from collections import deque
from typing import Any, Dict, List, Optional, Tuple

from ai_integration.core.node_classes import Landmark, Hotel
from ai_integration.core.problems import TravelProblem_LocalSearch

SKIP = "__SKIP__"


class CSP:
    """
    Abstract CSP.

    Subclasses set:
        self.variables  : list of variable names
        self.domains    : dict  var → [values]
        self.neighbors  : dict  var → [vars that share a binary constraint]
    and override:
        constraint(Xi, vi, Xj, vj) → bool
    """

    def __init__(self):
        self.variables:    List           = []
        self.domains:      Dict[Any, List] = {}
        self.neighbors:    Dict[Any, List] = {}
        self.nassigns:     int             = 0
        self.curr_domains: Optional[Dict]  = None   
        
    def constraint(self, Xi, vi, Xj, vj) -> bool:
        raise NotImplementedError

    def assign(self, var, val, assignment: dict):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment: dict):
        assignment.pop(var, None)

    def nconflicts(self, var, val, assignment: dict) -> int:
        """Number of neighbours whose current value conflicts with (var=val)."""
        return sum(
            1 for nb in self.neighbors[var]
            if nb in assignment
            and not self.constraint(var, val, nb, assignment[nb])
        )

    def support_pruning(self):
        """Copy domains into curr_domains on first call."""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value) -> List[Tuple]:
        """
        Restrict curr_domains[var] to [value].
        Returns the list of (var, pruned_val) pairs for later restore().
        """
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals: Optional[List]):
        """Remove value from curr_domains[var]; record it in removals."""
        if value in self.curr_domains[var]:
            self.curr_domains[var].remove(value)
            if removals is not None:
                removals.append((var, value))

    def choices(self, var) -> List:
        """Live values for var (curr_domains if pruning is active)."""
        return (self.curr_domains if self.curr_domains else self.domains)[var]

    def restore(self, removals: List[Tuple]):
        """Undo pruning by putting values back into curr_domains."""
        for var, val in removals:
            self.curr_domains[var].append(val)



def AC3(csp: CSP,
        queue:    Optional[deque] = None,
        removals: Optional[List]  = None) -> bool:
    """
    AC-3 arc-consistency algorithm.

    Enforces arc consistency across all (Xi, Xj) arcs.
    Returns False when an inconsistency is detected (empty domain).
    removals: pruned (var, val) pairs appended here so they can be restored.
    """
    if queue is None:
        queue = deque(
            (Xi, Xj)
            for Xi in csp.variables
            for Xj in csp.neighbors[Xi]
        )

    csp.support_pruning()

    while queue:
        Xi, Xj = queue.popleft()
        if _revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:        
                return False
            for Xk in csp.neighbors[Xi]:        
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True


def _revise(csp: CSP, Xi, Xj, removals) -> bool:
    """
    Remove from D(Xi) every value x for which no value y ∈ D(Xj) satisfies
    the arc (Xi, Xj).  Return True iff D(Xi) changed.
    """
    revised = False
    for x in list(csp.curr_domains[Xi]):
        if not any(csp.constraint(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised



def forward_checking(csp: CSP, var, value,
                     assignment: dict, removals: List) -> bool:
    """
    FORWARD-CHECKING .

    After var=value is assigned, remove from each unassigned neighbour's
    domain every value inconsistent with this assignment.
    Returns False if any neighbour's domain becomes empty.
    """
    csp.support_pruning()
    for Xj in csp.neighbors[var]:
        if Xj not in assignment:
            for vj in list(csp.curr_domains[Xj]):
                if not csp.constraint(var, value, Xj, vj):
                    csp.prune(Xj, vj, removals)
            if not csp.curr_domains[Xj]:
                return False
    return True

def mac(csp: CSP, var, value,
        assignment: dict, removals: List) -> bool:
    """
    MAC — Maintaining Arc Consistency.

    Seeds AC-3 with  { (Xj, var) : Xj is an unassigned neighbour of var }.
    Returns False if an inconsistency is detected.
    """
    queue = deque(
        (Xj, var)
        for Xj in csp.neighbors[var]
        if Xj not in assignment
    )
    return AC3(csp, queue=queue, removals=removals)

def mrv(csp: CSP, assignment: dict):
    """
    MRV — Minimum Remaining Values  (Norvig p.174).
    Pick the unassigned variable with the smallest live domain.
    Ties broken by the degree heuristic (most constraints on unassigned vars).
    """
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(
        unassigned,
        key=lambda v: (len(csp.choices(v)), -_degree(csp, v, assignment))
    )


def _degree(csp: CSP, var, assignment: dict) -> int:
    return sum(1 for nb in csp.neighbors[var] if nb not in assignment)


def first_unassigned(csp: CSP, assignment: dict):
    """Baseline: first unassigned variable in order."""
    for v in csp.variables:
        if v not in assignment:
            return v


def lcv(csp: CSP, var, assignment: dict) -> List:
    """
    LCV — Least Constraining Value.
    Order values so the one that rules out the fewest choices for
    neighbouring variables comes first.
    """
    return sorted(
        csp.choices(var),
        key=lambda v: csp.nconflicts(var, v, assignment)
    )


def identity_order(csp: CSP, var, assignment: dict) -> List:
    """Baseline: domain order."""
    return csp.choices(var)


def backtracking_search(
    csp:                        CSP,
    select_unassigned_variable  = mrv,
    order_domain_values         = lcv,
    inference                   = forward_checking,
    goal_test                   = None,
) -> Optional[dict]:
    """
    BACKTRACKING-SEARCH 

    Returns the first complete consistent assignment that passes goal_test,
    or None.

    goal_test: optional callable (assignment → bool).  When provided, a
               complete assignment is only accepted as a solution if
               goal_test(assignment) returns True.  This is the hook used
               by C5 (type-quota constraint) without modifying the core
               algorithm.

    function BACKTRACKING-SEARCH(csp) returns solution or failure
        return BACKTRACK({}, csp)

    function BACKTRACK(assignment, csp) returns solution or failure
        if assignment is complete then return assignment
        var ← SELECT-UNASSIGNED-VARIABLE(csp)
        for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
            if value is consistent with assignment then
                add {var = value} to assignment
                inferences ← INFERENCE(csp, var, value)
                if inferences ≠ failure then
                    add inferences to assignment
                    result ← BACKTRACK(assignment, csp)
                    if result ≠ failure then return result
                remove {var = value} and inferences from assignment
        return failure
    """

    def backtrack(assignment: dict) -> Optional[dict]:
        # Complete assignment → run goal test then accept or keep searching
        if len(assignment) == len(csp.variables):
            if goal_test is None or goal_test(assignment):
                return dict(assignment)
            return None   

        var = select_unassigned_variable(csp, assignment)

        for value in order_domain_values(csp, var, assignment):
            if csp.nconflicts(var, value, assignment) == 0:
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)

                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result              

                csp.restore(removals)
                csp.unassign(var, assignment)

        return None                                 

    csp.nassigns   = 0
    csp.curr_domains = None  

    csp.support_pruning()
    if not AC3(csp):
        return None            

    return backtrack({})



class TravelCSP(CSP):
    """
    CSP encoding of the tourist-routing problem.

    Variables : slots [0, 1, …, n-1]
    Domains   : D(i) = {candidate landmarks} ∪ {SKIP}
    Constraints (binary):
        C1 – AllDifferent  no two non-SKIP slots hold the same landmark
        C2 – SKIP-last     a SKIP slot cannot be followed by a non-SKIP slot
    Temporal constraints enforced inside inference (domain reduction):
        C3 – Time windows  landmark must be open at computed arrival time
        C4 – Budget        visit + return ≤ T_max
        C5 - Quota time
    """

    def __init__(
        self,
        problem:          TravelProblem_LocalSearch,
        inference_method: str             = "fc",    # 'fc' | 'mac'
        var_heuristic:    str             = "mrv",   # 'mrv' | 'none'
        val_heuristic:    str             = "lcv",   # 'lcv' | 'none'
        time_limit_s:     float           = 60.0,
        type_quota:       Optional[Dict[str, int]] = None,
    ):
        """
        Parameters
        ----------
        problem          : TravelProblem_LocalSearch instance.
        inference_method : 'fc' (Forward Checking) or 'mac' (MAC / AC-3).
        var_heuristic    : 'mrv' or 'none'.
        val_heuristic    : 'lcv' or 'none'.
        time_limit_s     : wall-clock seconds before giving up (0 = no limit).
        type_quota       : optional dict of minimum counts per landmark type.
                           e.g. {"mall": 2, "cultural": 3, "historical": 1}
                           means the solution must contain AT LEAST 2 malls,
                           3 cultural landmarks, and 1 historical landmark.
                           An error is raised if the quota is impossible to
                           satisfy (not enough candidates of a required type).
        """
        super().__init__()

        self.problem          = problem
        self.inference_method = inference_method
        self.var_heuristic    = var_heuristic
        self.val_heuristic    = val_heuristic
        self.time_limit_s     = time_limit_s
        self.type_quota: Dict[str, int] = type_quota or {}

        if problem.type_filter:
            self.candidates: List[Landmark] = [
                lm for lm in problem.landmarks
                if lm.landmark_type in problem.type_filter
            ]
        else:
            self.candidates = list(problem.landmarks)

        self.candidates.sort(key=lambda lm: lm.interest_score, reverse=True)

        if self.type_quota:
            available_by_type: Dict[str, int] = {}
            for lm in self.candidates:
                available_by_type[lm.landmark_type] = (
                    available_by_type.get(lm.landmark_type, 0) + 1
                )
            for lm_type, required in self.type_quota.items():
                available = available_by_type.get(lm_type, 0)
                if available < required:
                    raise ValueError(
                        f"type_quota cannot be satisfied: need {required} "
                        f"landmark(s) of type '{lm_type}' but only "
                        f"{available} candidate(s) exist."
                    )

        self.candidates.sort(key=lambda lm: lm.interest_score, reverse=True)

        n = len(self.candidates)
        self.variables = list(range(n))

        self.domains = {i: self.candidates + [SKIP] for i in self.variables}

        self.neighbors = {
            i: [j for j in self.variables if j != i]
            for i in self.variables
        }

        self._solution:  Optional[dict] = None
        self._timed_out: bool           = False
        self.nassigns:   int            = 0


    def constraint(self, Xi: int, vi, Xj: int, vj) -> bool:
        """
        C1 – AllDifferent: two non-SKIP slots must hold different landmarks.
        C2 – SKIP-last   : if the earlier of Xi/Xj is SKIP, the later must
                           also be SKIP (consecutive slots only).
        """
        if vi is not SKIP and vj is not SKIP and vi == vj:
            return False

        if abs(Xi - Xj) == 1:
            earlier_val = vi if Xi < Xj else vj
            later_val   = vj if Xi < Xj else vi
            if earlier_val is SKIP and later_val is not SKIP:
                return False

        return True

    def _reconstruct_time(self, up_to_slot: int, assignment: dict) -> float:
        current_time = self.problem.trip_start_time * 60.0
        prev_lm: Optional[Landmark] = None

        for s in range(up_to_slot):
            if s not in assignment or assignment[s] is SKIP:
                continue
            lm = assignment[s]
            src    = self.problem.hotel.name if prev_lm is None else prev_lm.name
            travel = self.problem.time_matrix[src][lm.name]
            arrival = current_time + travel

            try:
                is_open = lm.is_open(self.problem.Travel_day, arrival % 1440)
            except KeyError:
                current_time = arrival + lm.visit_duration
                prev_lm = lm
                continue

            if not is_open:
                opening = lm.opening_hours.get(self.problem.Travel_day)
                if opening:
                    hour = int(arrival // 60) + 1
                    while hour < 24:
                        if opening[hour % 24] == 1:
                            arrival = float(hour * 60)
                            break
                        hour += 1

            current_time = arrival + lm.visit_duration
            prev_lm = lm

        return current_time


    def _is_temporally_feasible(
        self, slot: int, landmark: Landmark, assignment: dict
    ) -> bool:
        current_time = self._reconstruct_time(slot, assignment)

        prev_lm: Optional[Landmark] = None
        for s in range(slot - 1, -1, -1):
            if s in assignment and assignment[s] is not SKIP:
                prev_lm = assignment[s]
                break

        src     = self.problem.hotel.name if prev_lm is None else prev_lm.name
        travel  = self.problem.time_matrix[src][landmark.name]
        arrival = current_time + travel

        try:
            is_open = landmark.is_open(self.problem.Travel_day, arrival % 1440)
        except KeyError:
            return False   

        if not is_open:
            opening = landmark.opening_hours.get(self.problem.Travel_day)
            if opening is None:
                return False
            hour   = int(arrival // 60) + 1
            opened = False
            while hour < 24:
                if opening[hour % 24] == 1:
                    arrival = float(hour * 60)
                    opened  = True
                    break
                hour += 1
            if not opened:
                return False

        ret     = self.problem.time_matrix[landmark.name][self.problem.hotel.name]
        finish  = arrival + landmark.visit_duration + ret
        elapsed = (finish / 60.0) - self.problem.trip_start_time
        return elapsed <= self.problem.max_travel_time

    def _prune_temporal(self, slot: int, assignment: dict,
                         removals: List) -> bool:
        """
        Remove from D(slot) every non-SKIP value that is temporally
        infeasible given the current assignment prefix.
        Returns False if the domain is wiped out.
        """
        self.support_pruning()
        for lm in list(self.curr_domains[slot]):
            if lm is SKIP:
                continue
            if not self._is_temporally_feasible(slot, lm, assignment):
                self.prune(slot, lm, removals)
        return bool(self.curr_domains[slot])


    def _quota_feasible(self, assignment: dict) -> bool:
        """
        Forward-looking check for C5 (type quota).

        For each required type t with quota q:
          • already_assigned[t]  = non-SKIP landmarks of type t already in
                                   the assignment.
          • still_possible[t]    = distinct landmarks of type t that appear
                                   in at least one UNASSIGNED slot's live domain.

        If already_assigned[t] + still_possible[t] < q for any t, the quota
        can never be reached from this partial assignment → return False.

        This is called inside every INFERENCE step, giving the same early-
        failure behaviour as forward checking but for a global constraint.
        """
        if not self.type_quota:
            return True

        assigned_counts: Dict[str, int] = {}
        for lm in assignment.values():
            if lm is not SKIP:
                assigned_counts[lm.landmark_type] = (
                    assigned_counts.get(lm.landmark_type, 0) + 1
                )

        possible_by_type: Dict[str, set] = {}
        for slot in self.variables:
            if slot in assignment:
                continue
            for lm in self.choices(slot):
                if lm is SKIP:
                    continue
                if lm.landmark_type not in possible_by_type:
                    possible_by_type[lm.landmark_type] = set()
                possible_by_type[lm.landmark_type].add(lm.id)


        for lm_type, required in self.type_quota.items():
            have     = assigned_counts.get(lm_type, 0)
            possible = len(possible_by_type.get(lm_type, set()))
            if have + possible < required:
                return False

        return True

    def _quota_satisfied(self, assignment: dict) -> bool:
        """
        Goal test for C5: checks that the complete assignment actually meets
        every minimum-count requirement.

        Called by backtracking_search when the assignment is complete.
        Returns False if any required type is under-represented, so the
        search backtracks and continues looking.
        """
        if not self.type_quota:
            return True

        counts: Dict[str, int] = {}
        for lm in assignment.values():
            if lm is not SKIP:
                counts[lm.landmark_type] = counts.get(lm.landmark_type, 0) + 1

        return all(
            counts.get(lm_type, 0) >= required
            for lm_type, required in self.type_quota.items()
        )

    def _inference_fc(self, csp: "TravelCSP", var: int, value,
                      assignment: dict, removals: List) -> bool:
        """
        FORWARD-CHECKING for C1/C2, temporal pruning on the next slot,
        and quota feasibility check for C5.
        """
        if not forward_checking(csp, var, value, assignment, removals):
            return False
        next_slot = var + 1
        if next_slot in csp.variables and next_slot not in assignment:
            if not csp._prune_temporal(next_slot, assignment, removals):
                return False
        if not csp._quota_feasible(assignment):
            return False
        return True

    def _inference_mac(self, csp: "TravelCSP", var: int, value,
                       assignment: dict, removals: List) -> bool:
        """
        MAC for C1/C2, temporal pruning on the next slot, and quota check.
        """
        if not mac(csp, var, value, assignment, removals):
            return False
        next_slot = var + 1
        if next_slot in csp.variables and next_slot not in assignment:
            if not csp._prune_temporal(next_slot, assignment, removals):
                return False
        # C5: can the remaining live domains still satisfy the quota?
        if not csp._quota_feasible(assignment):
            return False
        return True

    def solve(self) -> List[Landmark]:
        """Run BACKTRACKING-SEARCH and return the itinerary found."""
        var_fn = mrv           if self.var_heuristic    == "mrv" else first_unassigned
        val_fn = lcv           if self.val_heuristic    == "lcv" else identity_order
        inf_fn = self._inference_mac if self.inference_method == "mac" else self._inference_fc

        self._solution = backtracking_search(
            csp=self,
            select_unassigned_variable=var_fn,
            order_domain_values=val_fn,
            inference=inf_fn,
            goal_test=self._quota_satisfied,   # C5: accept only quota-meeting solutions
        )

        if not self._solution:
            return []
        return [
            self._solution[s]
            for s in sorted(self._solution)
            if self._solution[s] is not SKIP
        ]

    def stats(self) -> dict:
        itinerary = self.solve.__self__ and [
            self._solution[s]
            for s in sorted(self._solution or {})
            if (self._solution or {}).get(s) is not SKIP
        ] or []
        return {
            "landmarks_visited" : len(itinerary),
            "itinerary"         : [lm.name for lm in itinerary],
            "total_score"       : sum(lm.interest_score for lm in itinerary),
            "total_time_h"      : round(self._elapsed_hours(self._solution or {}), 2),
            "assignments_made"  : self.nassigns,
            "inference"         : self.inference_method,
            "var_heuristic"     : self.var_heuristic,
            "val_heuristic"     : self.val_heuristic,
        }

    def _elapsed_hours(self, assignment: dict) -> float:
        itinerary = [
            assignment[s]
            for s in sorted(k for k in assignment if assignment[k] is not SKIP)
        ]
        if not itinerary:
            return 0.0
        total = self.problem.time_matrix[self.problem.hotel.name][itinerary[0].name]
        for i, lm in enumerate(itinerary):
            total += lm.visit_duration
            if i < len(itinerary) - 1:
                total += self.problem.time_matrix[lm.name][itinerary[i + 1].name]
        total += self.problem.time_matrix[itinerary[-1].name][self.problem.hotel.name]
        return total / 60.0
