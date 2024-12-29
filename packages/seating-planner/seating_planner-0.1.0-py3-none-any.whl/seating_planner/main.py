from .model import SeatingPlanner
from .utils import load_guest_data, load_preferences_conflicts, print_results

def run(guest_data_path: str = "./katilimcilar.csv",
        preferences_path: str = "./preference_conflicts.json"):
    """
    Run the seating optimization.
    
    Args:
        guest_data_path: Path to the CSV file containing guest data
        preferences_path: Path to the JSON file containing preferences and conflicts
    """
    # Load data
    guest_groups = load_guest_data(guest_data_path)
    preferences, conflicts = load_preferences_conflicts(preferences_path)
    
    # Prepare data dictionary
    data = {
        'guest_groups': guest_groups,
        'preferences': preferences,
        'conflicts': conflicts,
        'priorities': {
            "Altay Ünal": 0,
            "Bilal Sivik": 0,
            "Melih Sarıkaya": 0,
            "Gürkan Aile": 0,
            "Erdoğan Güler": 1
        },
        'tables': {
            f"Table_{i}": 12 for i in range(1, 23)
        } | {
            f"Table_{i}": 16 for i in range(23, 28)
        } | {
            f"Table_{i}": 14 for i in range(28, 31)
        },
        'penalty_weights': {
            'over_capacity': 50,
            'under_capacity': 1,
            'conflict': 50,
            'preference': 100
        }
    }
    
    # Create planner, run optimization and get results
    planner = SeatingPlanner(data=data)
    results = planner.run()
    
    # Print results
    print_results(results, planner)

if __name__ == "__main__":
    run() 