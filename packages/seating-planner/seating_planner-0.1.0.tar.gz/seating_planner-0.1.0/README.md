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

data = {
    'guest_groups': {
        'Guest1': 2,  # Guest1 is a group of 2 people
        'Guest2': 1,  # Guest2 is a single person
        # ...
    },
    'tables': {
        'Table1': 8,  # Table1 has capacity of 8
        'Table2': 10, # Table2 has capacity of 10
        # ...
    },
    'preferences': [
        ('Guest1', 'Guest2'),  # Guest1 and Guest2 prefer to sit together
    ],
    'conflicts': [
        ('Guest3', 'Guest4'),  # Guest3 and Guest4 should not sit together
    ],
    'priorities': {
        'Guest1': 0,  # Higher priority guest (lower number = higher priority)
        'Guest2': 1,
    }
}

# Create planner and run optimization
planner = SeatingPlanner(data=data)
results = planner.run()
```

### Using CSV and JSON Files
```python
from seating_planner import run

# Run with default file paths
run()

# Or specify custom paths
run(
    guest_data_path="path/to/guests.csv",
    preferences_path="path/to/preferences.json"
)
```

## Data Format

### Guest Data (CSV)
The guest data should be in a CSV file with the following format:

```csv
Katılımcı Adı,Katılımcı Sayısı
John Smith,2
Jane Doe,1
Smith Family,4
```

Required columns:
- `Katılımcı Adı`: Guest/group name
- `Katılımcı Sayısı`: Number of people in the group

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
</rewritten_file>