import pandas as pd
import json

def add_price_per_area(data):
    for item in data:
        price = item['Place-Info']['Price']
        area = item['Place-Info']['Area of Place']
        price_per_area = price / area if area != 0 else 0
        item['Place-Info']['Price/Area'] = round(price_per_area, 2)
    return data

def add_price_per_room(data):
    for item in data:
        price = item['Place-Info']['Price']
        rooms = item['Place-Info']['Number of Rooms']
        price_per_room = price / rooms if rooms != 0 else 0
        item['Place-Info']['Price/Room'] = round(price_per_room, 2)
    return data

def add_total_cost(data):
    for item in data:
        price = item['Place-Info']['Price']
        monthly_spending = item['Place-Info']['Monthly Spending']
        total_cost = price + monthly_spending
        item['Place-Info']['Total Cost'] = round(total_cost, 2)
    return data
def add_yearly_cost(data):
    for item in data:
        total_cost = item['Place-Info']['Total Cost']
        yearly_cost = total_cost * 12
        item['Place-Info']['Yearly Cost'] = round(yearly_cost, 2)
    return data

def add_yearly_cost_per_area(data):
    for item in data:
        yearly_cost = item['Place-Info']['Yearly Cost']
        area = item['Place-Info']['Area of Place']
        yearly_price_per_area = yearly_cost / area if area != 0 else 0
        item['Place-Info']['Yearly Price/Area'] = round(yearly_price_per_area, 2)
    return data
def create_table_from_json(json_file):
    # Read data from JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Add Price/Area, Price/Room, Total Cost, yearly cot to each dictionary
    data = add_price_per_area(data)
    data = add_price_per_room(data)
    data = add_total_cost(data)
    data = add_yearly_cost(data)
    data = add_yearly_cost_per_area(data)

    # Create DataFrame from the JSON data
    df = pd.DataFrame([{
        'Post Name': item['Place-Info']['Post Name'],
        'Number of Rooms': item['Place-Info']['Number of Rooms'],
        'Area of Place': item['Place-Info']['Area of Place'],
        'Monthly Spending': item['Place-Info']['Monthly Spending'],
        'Price': item['Place-Info']['Price'],
        'Price/Area': item['Place-Info']['Price/Area'],
        'Price/Room': item['Place-Info']['Price/Room'],
        'Total Cost': item['Place-Info']['Total Cost']
        'Yearly Cost': item['Place-Info']['Yearly Cost']
    } for item in data])

    # Save DataFrame as an HTML file
    return df.to_html('data.html')
