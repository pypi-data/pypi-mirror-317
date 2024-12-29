# Seating Planner

A Python package for optimizing seating arrangements using linear programming.

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

# Prepare data dictionary
data = {
    'guest_groups': guest_groups,
    'preferences': preferences,
    'conflicts': conflicts,
    'tables': {
        'Table1': 8,  # Table1 has capacity of 8
        'Table2': 10, # Table2 has capacity of 10
    },
    'priorities': {
        'Guest1': 0,  # Higher priority guest (lower number = higher priority)
        'Guest2': 1,
    }
}

# Create planner and run optimization
planner = SeatingPlanner(data=data)
results = planner.run(
    solver='HIGHS',     # Optional: Choose solver ('HIGHS', 'GUROBI', 'GLPK', 'CBC', 'CPLEX')
    time_limit=300,     # Optional: Set time limit in seconds
    print_output=True   # Optional: Print results after solving
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
- `'GLPK'`: GNU Linear Programming Kit
- `'GUROBI'`: Commercial solver (requires license)
- `'CPLEX'`: Commercial solver (requires license)

Example with solver selection:
```python
results = planner.run(solver='GLPK', time_limit=300)
```

## Example Output

When `print_output=True`, the results will be displayed in this format:

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
results = planner.run(print_output=False)

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