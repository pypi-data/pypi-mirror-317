import pandas as pd
import json
from typing import Dict, List, Tuple
from seating_planner.model import SeatingPlanner

def load_guest_data(csv_path: str) -> Dict[str, int]:
    data = pd.read_csv(csv_path)
    return dict(zip(data["guest_name"], data["number_of_people"]))

def load_preferences_conflicts(json_path: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        preferences = [tuple(conf) for conf in data['preferences']]
        conflicts = [tuple(conf) for conf in data['conflicts']]
    return preferences, conflicts

def print_results(results: dict, planner: SeatingPlanner) -> None:
    """Pretty print the seating arrangement results."""
    print("\n" + "="*80)
    print(f"SEATING ARRANGEMENT RESULTS".center(80))
    print("="*80 + "\n")

    # Print solver status and handle infeasible case
    print(f"Solver Status: {results['status']}")
    if results['status'] == 'Infeasible':
        print("\n⚠️  The seating arrangement problem is INFEASIBLE!")
        print("This means no valid solution exists with the current constraints.")
        print("\nPossible reasons:")
        print("• Total table capacity is less than total number of guests")
        print("• Conflicting constraints that cannot be satisfied simultaneously")
        print("• Too many mandatory preferences that cannot all be met")
        
        # Print capacity analysis
        total_capacity = sum(planner.tables.values())
        total_guests = sum(planner.guest_groups.values())
        print(f"\nCapacity Analysis:")
        print(f"• Total Available Seats: {total_capacity}")
        print(f"• Total Guests: {total_guests}")
        if total_guests > total_capacity:
            print(f"❌ Not enough seats! Need {total_guests - total_capacity} more seats")
        print("\n" + "="*80)
        return

    # Print solver status and objective
    print(f"Solver Status: {results['status']}")
    print(f"Total Penalty Score: {results['objective_value']:.2f}")
    
    # Calculate and print overall utilization
    total_capacity = sum(planner.tables.values())
    total_guests = sum(planner.guest_groups.values())
    total_seats_used = sum(
        sum(planner.guest_groups.get(guest, 1) for guest in data['guests'])
        for data in results['assignments'].values()
    )
    
    print("\n" + "-"*80)
    print("OVERALL STATISTICS".center(80))
    print("-"*80)
    print(f"Total Available Seats: {total_capacity}")
    print(f"Total Guests: {total_guests}")
    print(f"Total Seats Used: {total_seats_used}")
    print(f"Overall Utilization: {(total_seats_used/total_capacity)*100:.1f}%")
    print("-"*80 + "\n")

    # Print table assignments
    print("TABLE ASSIGNMENTS".center(80))
    print("-"*80)
    
    for table, data in sorted(results['assignments'].items()):
        capacity = planner.tables[table]
        
        # Calculate total people at table
        total_people = sum(planner.guest_groups.get(guest, 1) for guest in data['guests'])
        utilization = (total_people / capacity) * 100
        
        print(f"\n📋 {table} (Capacity: {capacity} seats)")
        print(f"   Utilization: {utilization:.1f}% ({total_people}/{capacity} seats)")
        print(f"   Guests ({len(data['guests'])} groups, {total_people} total people):")
        for guest in data['guests']:
            group_size = planner.guest_groups.get(guest, 1)
            group_text = f"({group_size} people)" if group_size > 1 else "(1 person)"
            print(f"   • {guest} {group_text}")
        
        if data['over_capacity'] > 0:
            print(f"   ⚠️  Over Capacity by {data['over_capacity']} seats")
        if data['under_capacity'] > 0:
            print(f"   ⚠️  Under Capacity by {data['under_capacity']} seats")

    # Print violations
    if results['violations']['conflicts'] or results['violations']['preferences']:
        print("\n" + "-"*80)
        print("CONSTRAINT VIOLATIONS".center(80))
        print("-"*80)

        if results['violations']['conflicts']:
            print("\n🚫 Conflict Violations:")
            for violation in results['violations']['conflicts']:
                g1, g2 = violation['guests']
                g1_size = planner.guest_groups.get(g1, 1)
                g2_size = planner.guest_groups.get(g2, 1)
                print(f"   • {g1} ({g1_size} people) and {g2} ({g2_size} people) "
                      f"are seated together (Penalty: {violation['penalty']:.2f})")

        if results['violations']['preferences']:
            print("\n⚠️  Preference Violations:")
            for violation in results['violations']['preferences']:
                g1, g2 = violation['guests']
                g1_size = planner.guest_groups.get(g1, 1)
                g2_size = planner.guest_groups.get(g2, 1)
                print(f"   • {g1} ({g1_size} people) and {g2} ({g2_size} people) "
                      f"are not seated together (Penalty: {violation['penalty']:.2f})")

    print("\n" + "="*80) 