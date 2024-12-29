import pytest
from seating_planner import SeatingPlanner

@pytest.fixture
def sample_data():
    return {
        'guest_groups': {
            'Group1': 2,
            'Group2': 1,
            'Group3': 2,
        },
        'tables': {
            'Table1': 4,
            'Table2': 4,
        },
        'preferences': [
            ('Group1', 'Group2'),
        ],
        'conflicts': [
            ('Group2', 'Group3'),
        ],
        'priorities': {
            'Group1': 0,
            'Group2': 1,
            'Group3': 2,
        }
    }

def test_seating_planner_initialization(sample_data):
    planner = SeatingPlanner(data=sample_data)
    assert planner.guest_groups == sample_data['guest_groups']
    assert planner.tables == sample_data['tables']
    assert planner.preferences == sample_data['preferences']
    assert planner.conflicts == sample_data['conflicts']

def test_seating_planner_validation(sample_data):
    planner = SeatingPlanner(data=sample_data)
    result = planner.run()
    
    # Check if all guests are assigned
    assigned_guests = set()
    for table, guests in result.items():
        assigned_guests.update(guests)
    assert assigned_guests == set(sample_data['guest_groups'].keys())
    
    # Check table capacity constraints
    for table, guests in result.items():
        total_guests = sum(sample_data['guest_groups'][g] for g in guests)
        assert total_guests <= sample_data['tables'][table]
    
    # Check conflicts are respected
    for table, guests in result.items():
        for conflict_pair in sample_data['conflicts']:
            assert not (conflict_pair[0] in guests and conflict_pair[1] in guests)

def test_invalid_data():
    invalid_data = {
        'guest_groups': {'Group1': 5},
        'tables': {'Table1': 2},  # Not enough capacity
        'preferences': [],
        'conflicts': [],
        'priorities': {'Group1': 0}
    }
    
    planner = SeatingPlanner(data=invalid_data)
    with pytest.raises(Exception):
        planner.run() 