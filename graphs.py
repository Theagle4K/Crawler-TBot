import pandas as pd
import matplotlib.pyplot as plt

def plot_price_per_area(data):
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Price'], df['Area of Place'], color='blue')
    plt.title('Price vs Area')
    plt.xlabel('Price')
    plt.ylabel('Area of Place')
    plt.grid(True)
    plt.savefig('price_vs_area.png')
    plt.close()

def plot_price_per_rooms(data):
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Price'], df['Number of Rooms'], color='green')
    plt.title('Price vs Number of Rooms')
    plt.xlabel('Price')
    plt.ylabel('Number of Rooms')
    plt.grid(True)
    plt.savefig('price_vs_rooms.png')
    plt.close()
