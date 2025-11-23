"""
Data loading and preprocessing utilities.
"""

import pandas as pd
import os

def load_news_data(filepath='../data/raw_analyst_ratings.csv'):
    """Load and preprocess financial news data"""
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'], format='mixed', utc=True)
    return df

def load_stock_data(symbol, data_dir='../data/Data/'):
    """Load stock price data for given symbol"""
    filepath = os.path.join(data_dir, f'{symbol}.csv')
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

if __name__ == "__main__":
    print("Data loader module ready")
