import pandas as pd
import json


def create_table_from_json(json_file):
    # Read data from JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create DataFrame from the JSON data
    df = pd.DataFrame([{
        'Post Name': item['Place-Info']['Post Name'],
        'Number of Rooms': item['Place-Info']['Number of Rooms'],
        'Area of Place': item['Place-Info']['Area of Place'],
        'Montly Spending': item['Place-Info']['Montly Spending'],
        'Price': item['Place-Info']['Price']
    } for item in data])

    return df.to_html('data.html')
