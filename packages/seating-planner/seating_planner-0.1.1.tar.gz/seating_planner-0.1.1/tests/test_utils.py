import pytest
import pandas as pd
import json
from seating_planner.utils import load_guest_data, load_preferences
from pathlib import Path

@pytest.fixture
def sample_csv(tmp_path):
    csv_content = """guest_name,number_of_people
Group1,2
Group2,1
Group3,2"""
    csv_file = tmp_path / "guests.csv"
    csv_file.write_text(csv_content)
    return csv_file

@pytest.fixture
def sample_json(tmp_path):
    json_content = {
        "preferences": [
            ["Group1", "Group2"]
        ],
        "conflicts": [
            ["Group2", "Group3"]
        ]
    }
    json_file = tmp_path / "preferences_conflicts.json"
    json_file.write_text(json.dumps(json_content))
    return json_file

def test_load_guest_data(sample_csv):
    guest_data = load_guest_data(sample_csv)
    assert isinstance(guest_data, dict)
    assert guest_data['Group1'] == 2
    assert guest_data['Group2'] == 1
    assert guest_data['Group3'] == 2

def test_load_preferences(sample_json):
    prefs, conflicts = load_preferences(sample_json)
    assert prefs == [("Group1", "Group2")]
    assert conflicts == [("Group2", "Group3")]

def test_invalid_csv(tmp_path):
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("Invalid,CSV,Format")
    
    with pytest.raises(Exception):
        load_guest_data(invalid_csv)

def test_invalid_json(tmp_path):
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("invalid json")
    
    with pytest.raises(Exception):
        load_preferences(invalid_json) 