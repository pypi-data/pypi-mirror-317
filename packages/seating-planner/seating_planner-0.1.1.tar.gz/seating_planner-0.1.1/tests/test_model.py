import pytest
from seating_planner import SeatingPlanner
import pulp

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
    assert planner.priorities == sample_data['priorities']

def test_initialization_with_kwargs():
    planner = SeatingPlanner(
        guest_groups={'A': 1, 'B': 2},
        tables={'T1': 4},
        solver='HIGHS',
        time_limit=300
    )
    assert planner.guest_groups == {'A': 1, 'B': 2}
    assert planner.tables == {'T1': 4}
    assert planner.solver == 'HIGHS'
    assert planner.time_limit == 300

def test_table_generation():
    planner = SeatingPlanner()
    table_configs = {2: 8, 3: 10}  # 2 tables with 8 seats, 3 with 10 seats
    tables = planner.generate_tables(table_configs)
    
    assert len(tables) == 5  # Total number of tables
    assert sum(1 for t, c in tables.items() if c == 8) == 2
    assert sum(1 for t, c in tables.items() if c == 10) == 3

def test_solver_selection():
    planner = SeatingPlanner(data=sample_data)
    
    # Test different solver strings
    for solver_name in ['HIGHS', 'CBC', 'GLPK']:
        result = planner.run(solver=solver_name, print_output=False)
        assert result['status'] in ['Optimal', 'Not Solved']

def test_warmup_solution():
    data = {
        'guest_groups': {'A': 1, 'B': 1, 'C': 1},
        'tables': {'T1': 2, 'T2': 2},
    }
    warmup = {'A': 'T1'}  # Force guest A to be at table T1
    
    planner = SeatingPlanner(data=data, warmup_solution=warmup)
    result = planner.run(print_output=False)
    
    assert 'A' in result['assignments']['T1']['guests']

def test_capacity_constraints(sample_data):
    planner = SeatingPlanner(data=sample_data)
    result = planner.run(print_output=False)
    
    # Check if any table is over capacity
    for table, data in result['assignments'].items():
        guests = data['guests']
        capacity = sample_data['tables'][table]
        total_size = sum(sample_data['guest_groups'][g] for g in guests)
        assert total_size <= capacity + data['over_capacity']

def test_conflict_constraints(sample_data):
    planner = SeatingPlanner(data=sample_data)
    result = planner.run(print_output=False)
    
    # Check if conflicting guests are seated together
    for table, data in result['assignments'].items():
        guests = data['guests']
        for g1, g2 in sample_data['conflicts']:
            # If both guests are at this table, there should be a violation recorded
            if g1 in guests and g2 in guests:
                violation_found = any(
                    v['guests'] == (g1, g2) 
                    for v in result['violations']['conflicts']
                )
                assert violation_found

def test_preference_satisfaction(sample_data):
    planner = SeatingPlanner(data=sample_data)
    result = planner.run(print_output=False)
    
    # Check if preferred pairs are seated together when possible
    for g1, g2 in sample_data['preferences']:
        together = False
        for data in result['assignments'].values():
            if g1 in data['guests'] and g2 in data['guests']:
                together = True
                break
        # If not together, should be in violations
        if not together:
            violation_found = any(
                v['guests'] == (g1, g2) 
                for v in result['violations']['preferences']
            )
            assert violation_found

def test_invalid_solver():
    planner = SeatingPlanner(data=sample_data)
    with pytest.raises(ValueError, match="Unsupported solver"):
        planner.run(solver='INVALID_SOLVER')

def test_time_limit():
    # Create a problem that might take longer to solve
    large_data = {
        'guest_groups': {f'G{i}': 1 for i in range(50)},
        'tables': {f'T{i}': 10 for i in range(10)},
        'preferences': [(f'G{i}', f'G{i+1}') for i in range(0, 49, 2)],
        'conflicts': [(f'G{i}', f'G{i+1}') for i in range(1, 49, 2)]
    }
    
    planner = SeatingPlanner(data=large_data)
    result = planner.run(time_limit=1, print_output=False)  # 1 second limit
    
    # Should have a result, even if not optimal
    assert result['status'] in ['Optimal', 'Not Solved', 'Time Limit']

def test_empty_data():
    with pytest.raises(ValueError):
        SeatingPlanner(data={'guest_groups': {}})  # Missing tables
    
    with pytest.raises(ValueError):
        SeatingPlanner(data={'tables': {}})  # Missing guest_groups 