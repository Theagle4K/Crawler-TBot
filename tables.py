import pandas as pd
import json

def add_price_per_area(data):
    for item in data:
        price = item['Place-Info']['Price']
        area = item['Place-Info']['Area of Place']
        price_per_area = price / area if area != 0 else 0
        item['Place-Info']['Price/Area'] = price_per_area
    return data

def create_table_from_json(json_file):
    # Read data from JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Add Price/Area to each dictionary
    data = add_price_per_area(data)

    # Create DataFrame from the JSON data
    df = pd.DataFrame([{
        'Post Name': item['Place-Info']['Post Name'],
        'Number of Rooms': item['Place-Info']['Number of Rooms'],
        'Area of Place': item['Place-Info']['Area of Place'],
        'Montly Spending': item['Place-Info']['Montly Spending'],
        'Price': item['Place-Info']['Price'],
        'Price/Area': item['Place-Info']['Price/Area']
    } for item in data])

    # Save DataFrame as an HTML file
    return df.to_html('data.html')

