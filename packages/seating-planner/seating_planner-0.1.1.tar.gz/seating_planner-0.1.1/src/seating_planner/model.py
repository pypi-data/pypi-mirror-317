import pulp
import pandas as pd
import json
from typing import Dict, List, Tuple, Optional

class SeatingPlanner:
    def __init__(self, data=None, **kwargs):
        """
        Initialize SeatingPlanner with optional parameters.
        
        Args:
            data: Dictionary containing base configuration:
                - guest_groups: Dict[str, int] of guest names and group sizes
                - preferences: List[Tuple[str, str]] of preferred seating pairs
                - conflicts: List[Tuple[str, str]] of conflicting pairs
                - priorities: Dict[str, int] of guest priorities (optional)
                - tables: Dict[str, int] of table names and capacities
                - penalty_weights: Dict[str, float] of penalty weights (optional)
            **kwargs: Additional configuration parameters:
                - solver: PuLP solver instance (default: HIGHS)
                - time_limit: Time limit in seconds
                - guest_groups: Alternative way to pass guest groups
                - preferences: Alternative way to pass preferences
                - conflicts: Alternative way to pass conflicts
                - priorities: Alternative way to pass priorities
                - tables: Alternative way to pass tables
                - penalty_weights: Alternative way to pass penalty weights
                - table_configs: Dict[int, int] for generating tables
        """
        # Initialize problem
        self.problem = pulp.LpProblem("WeddingSeating", pulp.LpMinimize)
        
        # Store solver settings
        self.solver = kwargs.get('solver', None)
        self.time_limit = kwargs.get('time_limit', None)
        
        # Initialize empty data structures
        self.guest_groups = kwargs.get('guest_groups', {})
        self.tables = kwargs.get('tables', {})
        self.preferences = kwargs.get('preferences', [])
        self.conflicts = kwargs.get('conflicts', [])
        self.priorities = kwargs.get('priorities', {})
        
        # Default penalty weights
        self.penalty_weights = {
            'over_capacity': 50,
            'under_capacity': 1,
            'conflict': 50,
            'preference': 100
        }
        
        # Update penalty weights if provided
        if 'penalty_weights' in kwargs:
            self.penalty_weights.update(kwargs['penalty_weights'])
        
        # Initialize with data dictionary if provided
        if data:
            self.initialize_from_data(data)
            
        # Generate tables if table_configs provided
        if 'table_configs' in kwargs:
            self.tables = self.generate_tables(kwargs['table_configs'])
            
        # Set warmup solution if provided
        if 'warmup_solution' in kwargs:
            self.set_warmup_solution(kwargs['warmup_solution'])
            
        # Initialize decision variables
        self.x = None
        self.over_capacity = None
        self.under_capacity = None
        self.conflict_violations = None
        self.preference_violations = None

    def initialize_from_data(self, data):
        """Initialize model with provided data dictionary."""
        # Required data
        if 'guest_groups' not in data or 'tables' not in data:
            raise ValueError("guest_groups and tables are required in data dictionary")
            
        self.guest_groups = data['guest_groups']
        self.tables = data['tables']
        
        # Optional data with defaults
        self.preferences = data.get('preferences', [])
        self.conflicts = data.get('conflicts', [])
        self.priorities = data.get('priorities', {})
        
        # Update penalty weights if provided
        if 'penalty_weights' in data:
            self.penalty_weights.update(data['penalty_weights'])
            
        # Filter preferences and conflicts to valid guests
        self.preferences = [
            (g1, g2) for g1, g2 in self.preferences 
            if g1 in self.guest_groups and g2 in self.guest_groups
        ]
        
        self.conflicts = [
            (g1, g2) for g1, g2 in self.conflicts 
            if g1 in self.guest_groups and g2 in self.guest_groups
        ]
        
        # Set default priorities for guests not specified
        self.priorities = {
            guest: self.priorities.get(guest, 100)
            for guest in self.guest_groups
        }

    def run(self, solver=None, time_limit=None, print_output=True):
        """Run the optimization and return results.
        
        Args:
            solver: Optional solver instance. Overrides the solver set during initialization.
            time_limit: Optional time limit in seconds. Overrides the time limit set during initialization.
            print_output: Whether to print results after solving. Defaults to True.
        
        Returns:
            Dictionary containing optimization results
        """
        self.create_variables()
        self.set_objective()
        self.add_constraints()
        # Use instance variables if no override provided
        solver = solver if solver is not None else self.solver
        time_limit = time_limit if time_limit is not None else self.time_limit
        self.solve(solver=solver, time_limit=time_limit)
        results = self.get_results()
        
        if print_output:
            from .utils import print_results
            print_results(results, self)
            
        return results

    def load_data(self, guest_groups: Dict[str, int], preferences: List[Tuple[str, str]], conflicts: List[Tuple[str, str]]):
        # Set data directly from parameters
        self.guest_groups = guest_groups
        
        # Filter preferences and conflicts to only include existing guests
        self.preferences = [
            (g1, g2) for g1, g2 in preferences 
            if g1 in self.guest_groups and g2 in self.guest_groups
        ]
        
        self.conflicts = [
            (g1, g2) for g1, g2 in conflicts 
            if g1 in self.guest_groups and g2 in self.guest_groups
        ]
        
        # Set default priorities
        self.priorities = {guest: 100 for guest in self.guest_groups}
        self._set_special_priorities()

    def _set_special_priorities(self, priority_guests: Dict[str, int] = None):
        """Set special priorities for specific guests."""
        if priority_guests:
            for guest, priority in priority_guests.items():
                self.priorities[guest] = priority

    def generate_tables(self, table_configs: Dict[int, int]) -> Dict[str, int]:
        """
        Generate tables based on size configurations
        
        Args:
            table_configs: Dictionary where key is number of tables and value is seats per table
                         e.g., {10: 8, 5: 12} means 10 tables with 8 seats and 5 tables with 12 seats
        
        Returns:
            Dictionary of table names and their capacities
        """
        tables = {}
        table_counter = 1
        
        for num_tables, seats in table_configs.items():
            for _ in range(num_tables):
                tables[f"Table_{table_counter}"] = seats
                table_counter += 1
                
        return tables

    def set_tables(self, tables: Optional[Dict[str, int]] = None, table_configs: Optional[Dict[int, int]] = None):
        """
        Set tables either directly or generate them from configuration
        
        Args:
            tables: Direct mapping of table names to capacities
            table_configs: Configuration for table generation {num_tables: seats_per_table}
        """
        if tables is not None:
            self.tables = tables
        elif table_configs is not None:
            self.tables = self.generate_tables(table_configs)
        else:
            raise ValueError("Either tables or table_configs must be provided")

    def set_warmup_solution(self, warmup: Dict[str, str]):
        # Filter warmup solution to only include existing guests and valid tables
        self.warmup_solution = {
            g: t for g, t in warmup.items() 
            if g in self.guest_groups and t in self.tables
        }

    def create_variables(self):
        self.x = pulp.LpVariable.dicts("Seat", 
            [(g, t) for g in self.guest_groups for t in self.tables], 
            cat="Binary")
        
        self.over_capacity = pulp.LpVariable.dicts("OverCapacity", 
            self.tables, lowBound=0, cat="Continuous")
        self.under_capacity = pulp.LpVariable.dicts("UnderCapacity", 
            self.tables, lowBound=0, cat="Continuous")
        self.conflict_violations = pulp.LpVariable.dicts("ConflictViolation", 
            self.conflicts, lowBound=0, cat="Continuous")
        self.preference_violations = pulp.LpVariable.dicts("PreferenceViolation", 
            self.preferences, lowBound=0, cat="Continuous")

    def set_objective(self):
        self.problem += (
            pulp.lpSum(self.penalty_weights['over_capacity'] * self.over_capacity[t] + 
                      self.penalty_weights['under_capacity'] * self.under_capacity[t] 
                      for t in self.tables) +
            pulp.lpSum(self.penalty_weights['conflict'] * self.conflict_violations[(g1, g2)] 
                      for g1, g2 in self.conflicts) +
            pulp.lpSum(self.penalty_weights['preference'] * self.preference_violations[(g1, g2)] 
                      for g1, g2 in self.preferences) -
            pulp.lpSum(self.priorities[g] * pulp.lpSum(self.x[(g, t)] 
                      for t in self.tables) for g in self.guest_groups)
        )

    def add_constraints(self):
        # Warmup constraints
        for g, t in self.warmup_solution.items():
            if g in self.guest_groups and t in self.tables:
                self.problem += self.x[(g, t)] == 1, f"WarmUp_{g}_to_{t}"

        # Assignment constraints
        for g in self.guest_groups:
            self.problem += pulp.lpSum(self.x[(g, t)] for t in self.tables) == 1, f"GuestAssignment_{g}"

        # Capacity constraints
        for t, capacity in self.tables.items():
            self.problem += (pulp.lpSum(self.guest_groups[g] * self.x[(g, t)] 
                           for g in self.guest_groups) - capacity <= 
                           self.over_capacity[t], f"OverCapacity_{t}")
            self.problem += (capacity - pulp.lpSum(self.guest_groups[g] * self.x[(g, t)] 
                           for g in self.guest_groups) <= 
                           self.under_capacity[t], f"UnderCapacity_{t}")

        # Conflict constraints
        for g1, g2 in self.conflicts:
            for t in self.tables:
                self.problem += (self.x[(g1, t)] + self.x[(g2, t)] <= 
                               1 + self.conflict_violations[(g1, g2)], 
                               f"RelaxedConflict_{g1}_{g2}_on_{t}")

        # Preference constraints
        for g1, g2 in self.preferences:
            for t in self.tables:
                self.problem += (self.x[(g1, t)] - self.x[(g2, t)] <= 
                               self.preference_violations[(g1, g2)], 
                               f"RelaxedPreference_{g1}_{g2}_on_{t}_1")
                self.problem += (self.x[(g2, t)] - self.x[(g1, t)] <= 
                               self.preference_violations[(g1, g2)], 
                               f"RelaxedPreference_{g1}_{g2}_on_{t}_2")

    def solve(self, solver=None, time_limit=None):
        """
        Solve the optimization problem using the specified solver.
        
        Args:
            solver: Optional solver name as string. Defaults to 'HIGHS' if not specified.
                   Supported solvers: 'HIGHS', 'GUROBI', 'GLPK', 'CPLEX', 'CBC'
            time_limit: Optional time limit in seconds. If None, no time limit is set.
                       Note: Not all solvers support time limits.
        
        Returns:
            problem status from solver
        """
        # Convert solver string to PuLP solver instance
        if isinstance(solver, str):
            solver = solver.upper()
            if solver == 'HIGHS':
                solver_instance = pulp.HIGHS()
            elif solver == 'GUROBI':
                solver_instance = pulp.GUROBI_CMD()
            elif solver == 'GLPK':
                solver_instance = pulp.GLPK_CMD()
            elif solver == 'CPLEX':
                solver_instance = pulp.CPLEX_CMD()
            elif solver == 'CBC':
                solver_instance = pulp.CBC_CMD()
            else:
                raise ValueError(f"Unsupported solver: {solver}. "
                               "Supported solvers: HIGHS, GUROBI, GLPK, CPLEX, CBC")
        elif solver is None:
            solver_instance = pulp.HIGHS()
        else:
            solver_instance = solver  # Assume it's already a PuLP solver instance

        if time_limit is not None:
            # Set time limit based on solver type
            if isinstance(solver_instance, pulp.HIGHS):
                solver_instance.timeLimit = time_limit
            elif isinstance(solver_instance, pulp.GUROBI_CMD):
                solver_instance.options = ['TimeLimit=' + str(time_limit)]
            elif isinstance(solver_instance, pulp.GLPK_CMD):
                solver_instance.options = ['--tmlim', str(time_limit)]
            elif isinstance(solver_instance, pulp.CPLEX_CMD):
                solver_instance.options = ['timelimit=' + str(time_limit)]
            elif isinstance(solver_instance, pulp.CBC_CMD):
                solver_instance.options = ['sec', str(time_limit)]
            
        self.problem.solve(solver_instance)
        return self.problem.status

    def get_results(self) -> Dict:
        results = {
            "status": pulp.LpStatus[self.problem.status],
            "objective_value": pulp.value(self.problem.objective),
            "assignments": {},
            "violations": {
                "conflicts": [],
                "preferences": []
            }
        }

        # Get table assignments
        for t in self.tables:
            assigned_guests = [g for g in self.guest_groups 
                             if pulp.value(self.x[(g, t)]) == 1]
            results["assignments"][t] = {
                "guests": assigned_guests,
                "over_capacity": int(pulp.value(self.over_capacity[t])),
                "under_capacity": int(pulp.value(self.under_capacity[t]))
            }

        # Get violations
        for g1, g2 in self.conflicts:
            if pulp.value(self.conflict_violations[(g1, g2)]) > 0:
                results["violations"]["conflicts"].append({
                    "guests": (g1, g2),
                    "penalty": pulp.value(self.conflict_violations[(g1, g2)])
                })

        for g1, g2 in self.preferences:
            if pulp.value(self.preference_violations[(g1, g2)]) > 0:
                results["violations"]["preferences"].append({
                    "guests": (g1, g2),
                    "penalty": pulp.value(self.preference_violations[(g1, g2)])
                })

        return results
