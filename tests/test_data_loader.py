"""
Unit tests for data loader functions
"""

import pandas as pd
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from data_loader import load_news_data, load_stock_data

class TestDataLoader:
    """Test data loading functionality"""
    
    def test_load_news_data_structure(self, tmp_path):
        """Test news data loading structure"""
        # Create temporary test CSV
        test_data = pd.DataFrame({
            'headline': ['Test Headline 1', 'Test Headline 2'],
            'date': ['2023-01-01 10:00:00', '2023-01-02 11:00:00'],
            'stock': ['AAPL', 'GOOGL'],
            'publisher': ['Test Pub'] * 2
        })
        
        test_file = tmp_path / "test_news.csv"
        test_data.to_csv(test_file, index=False)
        
        # Load and test
        df = load_news_data(str(test_file))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'date' in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df['date'])
    
    def test_load_stock_data_structure(self, tmp_path):
        """Test stock data loading structure"""
        # Create temporary test CSV
        test_data = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02'],
            'Close': [150.0, 155.0],
            'Open': [148.0, 153.0],
            'High': [152.0, 157.0],
            'Low': [147.0, 152.0],
            'Volume': [1000000, 1200000]
        })
        
        os.makedirs(tmp_path / "Data", exist_ok=True)
        test_file = tmp_path / "Data" / "AAPL.csv"
        test_data.to_csv(test_file, index=False)
        
        # Load and test
        df = load_stock_data('AAPL', str(tmp_path / "Data"))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'Date' in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df['Date'])