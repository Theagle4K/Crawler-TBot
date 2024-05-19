import pandas as pd
import json


def create_table_from_json(json_file):
    # Read data from JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create DataFrame from the JSON data
    df = pd.DataFrame([item['Place-Info'] for item in data])

    return df
