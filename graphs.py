import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def plot_price_per_area(data):
    # Extract relevant data
    data_dicts = [
        {
            'Price': item['Place-Info']['Price'],
            'Area of Place': item['Place-Info']['Area of Place']
        }
        for item in data
    ]
    df = pd.DataFrame(data_dicts)
    
    # Sorting the dataframe by Price to ensure proper line plotting
    df = df.sort_values(by='Price')
    
    # Plotting
    matplotlib.use('agg')
    plt.figure(figsize=(10, 6))
    plt.plot(df['Price'], df['Area of Place'], color='blue', marker='o')
    plt.title('Price vs Area')
    plt.xlabel('Price')
    plt.ylabel('Area of Place')
    plt.grid(True)
    plt.savefig('price_vs_area.png')
    plt.close()

def plot_price_per_rooms(data):
    # Extract relevant data
    data_dicts = [
        {
            'Price': item['Place-Info']['Price'],
            'Number of Rooms': item['Place-Info']['Number of Rooms']
        }
        for item in data
    ]
    df = pd.DataFrame(data_dicts)
    
    # Sorting the dataframe by Price
    df = df.sort_values(by='Price')
    
    # Plotting
    matplotlib.use('agg')
    plt.figure(figsize=(10, 6))
    plt.plot(df['Price'], df['Number of Rooms'], color='green', marker='o')
    plt.title('Price vs Number of Rooms')
    plt.xlabel('Price')
    plt.ylabel('Number of Rooms')
    plt.grid(True)
    plt.savefig('price_vs_rooms.png')
    plt.close()
