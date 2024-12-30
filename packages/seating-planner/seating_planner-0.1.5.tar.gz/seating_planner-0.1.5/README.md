# Seating Planner

A Python package for optimizing seating arrangements using linear programming. This tool helps solve the complex problem of assigning guests to tables while considering:
- Group sizes and table capacities
- Seating preferences between guests
- Conflicts between guests who should not be seated together
- Guest priority levels
- Table capacity constraints

The package uses mathematical optimization to find the best possible seating arrangement that maximizes guest satisfaction while minimizing constraint violations.

## Installation

```bash
pip install seating-planner
```

## Usage

### Basic Usage
```python
from seating_planner import SeatingPlanner
import pandas as pd
import json

# Read guest data from CSV
guests_df = pd.read_csv('guests.csv')
guest_groups = dict(zip(guests_df['guest_name'], guests_df['number_of_people']))

# Read preferences and conflicts from JSON
with open('preferences.json', 'r') as f:
    pref_data = json.load(f)
    preferences = pref_data['preferences']
    conflicts = pref_data['conflicts']

# Create planner and run optimization
planner = SeatingPlanner(
    guest_groups,
    preferences,
    conflicts,
    tables={
        'Table1': 8,  # Table1 has capacity of 8
        'Table2': 10, # Table2 has capacity of 10
    },
    priorities={
        'Guest1': 0,  # Higher priority guest (lower number = higher priority)
        'Guest2': 1,
    }
    solver='HIGHS',     # Optional: Choose solver ('HIGHS', 'GUROBI', 'CBC', 'CPLEX')
    time_limit=300,     # Optional: Set time limit in seconds
    print_output=True   # Optional: Print results after solving
    )
results = planner.run(

)
```

### Alternative Initialization
```python
# Initialize with individual parameters
planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables={'Table1': 8, 'Table2': 10},
    preferences=preferences,
    conflicts=conflicts,
    priorities={'Guest1': 0},
    solver='HIGHS',
    time_limit=300
)
results = planner.run()

# Or generate tables from configuration
planner = SeatingPlanner(
    guest_groups=guest_groups,
    table_configs={
        10: 8,  # 10 tables with 8 seats each
        5: 12   # 5 tables with 12 seats each
    },
    preferences=preferences,
    conflicts=conflicts
)
results = planner.run()
```

## Data Format

### Guest Data (CSV)
The guest data should be in a CSV file with the following format:

```csv
guest_name,number_of_people
John Smith,2
Jane Doe,1
Smith Family,4
```

Required columns:
- `guest_name`: Guest/group name
- `number_of_people`: Number of people in the group

### Preferences and Conflicts (JSON)
The preferences and conflicts should be defined in a JSON file with the following format:

```json
{
    "preferences": [
        ["John Smith", "Jane Doe"],     // These guests prefer to sit together
        ["Smith Family", "John Smith"]  // Another seating preference
    ],
    "conflicts": [
        ["Jane Doe", "Smith Family"],   // These guests should not sit together
        ["John Smith", "Guest X"]       // Another seating conflict
    ]
}
```

The JSON file contains two main arrays:
- `preferences`: List of pairs that prefer to sit together
- `conflicts`: List of pairs that should not sit together

Each pair is represented as an array of two guest names that must match the names in the CSV file.

## Available Solvers

The package supports multiple solvers:
- `'HIGHS'` (default): Open-source solver, comes with PuLP
- `'CBC'`: Open-source solver
- `'GUROBI'`: Commercial solver (requires license)
- `'CPLEX'`: Commercial solver (requires license)

Example with solver selection:
```python
planner = SeatingPlanner(
    guest_groups=guest_groups,
    table_configs={
        10: 8,  # 10 tables with 8 seats each
        5: 12   # 5 tables with 12 seats each
    },
    preferences=preferences,
    conflicts=conflicts,
    solver="HiGHS",
)
results = planner.run()
```

## Example Output

When `verbose=True`, the results will be displayed in this format:

```
=== Optimization Results ===
Status: Optimal
Objective Value: 123.45

=== Table Assignments ===
Table1:
  Guests (3): John Smith, Jane Doe, Bob Wilson
  Under Capacity: 1

Table2:
  Guests (4): Alice Brown, Charlie Davis, Smith Family
  Over Capacity: 2

Table3:
  Guests (2): Eve Johnson, David Lee

=== Conflict Violations ===
  Smith Family and Bob Wilson (penalty: 1.00)

=== Preference Violations ===
  John Smith and Smith Family (penalty: 0.50)
```

The output shows:
- Optimization status and objective value
- Assignments of guests to tables
- Any capacity violations (over/under)
- Any conflict violations (guests who shouldn't sit together but had to)
- Any preference violations (guests who preferred to sit together but couldn't)

You can also access these results programmatically from the returned dictionary:

```python
results = planner.run()

# Access optimization status
print(results['status'])  # 'Optimal'

# Access table assignments
for table, data in results['assignments'].items():
    print(f"\n{table}:")
    print(f"Guests: {data['guests']}")
    print(f"Over capacity: {data['over_capacity']}")
    print(f"Under capacity: {data['under_capacity']}")

# Access violations
for conflict in results['violations']['conflicts']:
    print(f"Conflict between: {conflict['guests']}")
    print(f"Penalty: {conflict['penalty']}")

for pref in results['violations']['preferences']:
    print(f"Preference not met: {pref['guests']}")
    print(f"Penalty: {pref['penalty']}")
```

## Advanced Features

### Warmup Solutions

The warmup solution feature allows you to provide an initial partial seating arrangement that the optimizer must respect. This is useful when:

- You have certain guests that must be seated at specific tables
- You want to fix part of a previous solution while re-optimizing the rest
- You're working with an iterative planning process

```python
# Example using warmup solution
warmup = {
    'John Smith': 'Table1',    # Force John Smith to be at Table1
    'Jane Doe': 'Table2'       # Force Jane Doe to be at Table2
}

planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables=tables,
    preferences=preferences,
    conflicts=conflicts,
    warmup_solution=warmup     # Pass the warmup solution
)
results = planner.run()
```

The warmup solution is a dictionary where:
- Keys are guest names
- Values are table names where those guests must be seated

Notes:
- Only valid guest-table pairs will be considered
- The optimizer will respect these assignments while optimizing the remaining seats
- If the warmup solution makes the problem infeasible, the solver will indicate this
- You can use warmup solutions to implement incremental planning strategies

### MIP Gap

The MIP gap parameter controls the trade-off between solution quality and solve time:

```python
planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables=tables,
    mip_gap=0.05  # Stop when solution is within 5% of optimal
)
```

- Smaller gap (e.g., 0.01): Better solutions but longer solve times
- Larger gap (e.g., 0.1): Faster solutions but potentially suboptimal
- Default: None (find optimal solution)

### Table Capacity Constraints

You can control how much a table's capacity can be exceeded using the `max_capacity_overflow` parameter:

```python
planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables={'Table1': 10, 'Table2': 8},
    max_capacity_overflow=0.3  # Allow max 30% overflow
)
```

This parameter sets a hard limit on table capacity overflow:
- Default value is 0.5 (50% overflow allowed)
- For example, with `max_capacity_overflow=0.3`:
  - A table with capacity 10 can seat maximum 13 people
  - A table with capacity 8 can seat maximum 10 people
- Set to 0 to enforce strict capacity limits
- The solver will return infeasible if it cannot find a solution within these limits

This helps ensure realistic solutions by preventing excessive table overcrowding. The optimizer will still try to minimize any overflow through the objective function's penalty terms.

Example with strict capacity limits:
```python
planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables=tables,
    max_capacity_overflow=0.0  # No overflow allowed
)
```

Example allowing flexible overflow:
```python
planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables=tables,
    max_capacity_overflow=0.5  # Allow up to 50% overflow
)
```

### Converting Results to DataFrame

You can convert the seating assignments to a pandas DataFrame for easier analysis:

```python
results = planner.run()
df = planner.to_dataframe(results)

# View assignments
print(df)
```

Example output:
```
   guest_name assigned_table  group_size
0  John Smith        Table1           2
1    Jane Doe        Table1           1
2     Group A        Table2           4
3     Group B        Table2           3
```

The DataFrame contains:
- `guest_name`: Name of the guest/group
- `assigned_table`: Name of the assigned table
- `group_size`: Number of people in the group

This format makes it easy to:
- Sort and filter assignments
- Export to Excel/CSV
- Create visualizations
- Perform further analysis

## Commercial Solver Support

### Gurobi

The package supports Gurobi as a solver, which often provides better performance for large problems. To use Gurobi:

1. Obtain a Gurobi license (free for academic use):
   - Visit [Gurobi's Academic Program](https://www.gurobi.com/academia/academic-program-and-licenses/)
   - Request an academic license
   - Follow their installation instructions

2. Set up the license:
```bash
# Option 1: Set environment variable
export GRB_LICENSE_FILE=/path/to/gurobi.lic

# Option 2: Place license file in default location
# Linux/Mac: $HOME/gurobi.lic
# Windows: C:\gurobi.lic
```

3. Use Gurobi in your code:
```python
planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables=tables,
    solver='GUROBI'  # Specify Gurobi as solver
)
```

### CPLEX

IBM CPLEX is another powerful commercial solver option:

1. Obtain a CPLEX license:
   - Visit [IBM Academic Initiative](https://www.ibm.com/academic/technology/data-science)
   - Register for an academic account
   - Download CPLEX Optimization Studio

2. Install CPLEX Python API:
```bash
pip install cplex
```

3. Use CPLEX in your code:
```python
planner = SeatingPlanner(
    guest_groups=guest_groups,
    tables=tables,
    solver='CPLEX'  # Specify CPLEX as solver
)
```

### Visualizations

The package includes a visualization function to create a pie chart showing the satisfaction levels of guest seating arrangements.

```python
chart = planner.visualize_overall_satisfaction()
chart.save('satisfaction_chart.html')
```
![Example Chart](examples/charts/satisfaction_chart.png)


### Solver Performance Comparison

Here's a comparison of solver performance across different implementations with around 380 guests and 3 different table sizes:

| Solver  | Avg Time (s) | Min Time (s) | Max Time (s) | Avg Objective | Best Objective | Worst Objective |
|---------|--------------|--------------|--------------|---------------|----------------|-----------------|
| CBC     | 601.61      | 601.42      | 601.97      | -18000.0     | -18000.0      | -18000.0       |
| GUROBI  | 3.59        | 3.32        | 4.14        | -18150.0     | -18150.0      | -18150.0       |
| HiGHS   | 63.05       | 62.56       | 63.61       | -18150.0     | -18150.0      | -18150.0       |

Key observations:
- **GUROBI** provides the fastest solution times by far (~3.6s) (So does CPLEX but it requires a license too)
- **HiGHS** offers reasonable performance (~63s) without requiring a commercial license
- **CBC** takes significantly longer (~600s) but reaches similar solution quality, however it is not recommended for large problems and benchmark test is done with a time limitation for CBC (600 seconds).
