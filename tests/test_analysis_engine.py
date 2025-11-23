"""
Simple tests for OOP analysis engine
"""

import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from analysis_engine import FinancialNewsAnalyzer, TechnicalAnalyzer

def test_analyzer_initialization():
    """Test that analyzer initializes correctly"""
    analyzer = FinancialNewsAnalyzer()
    assert analyzer.news_data is None
    assert analyzer.stock_data is None
    assert analyzer.merged_data is None
    print(" test_analyzer_initialization passed")

def test_sentiment_analysis():
    """Test sentiment analysis method"""
    analyzer = FinancialNewsAnalyzer()
    
    # Test positive sentiment
    positive_score = analyzer.analyze_sentiment("Apple stock surges to record high")
    assert positive_score > 0
    
    # Test negative sentiment  
    negative_score = analyzer.analyze_sentiment("Apple stock plunges on weak earnings")
    assert negative_score < 0
    
    # Test edge cases
    assert analyzer.analyze_sentiment("") == 0.0
    assert analyzer.analyze_sentiment(123) == 0.0
    
    print(" test_sentiment_analysis passed")

def test_technical_analyzer():
    """Test technical analyzer"""
    # Create sample stock data
    sample_data = pd.DataFrame({
        'Close': [100, 102, 101, 105, 107, 106, 108, 110, 109, 111],
        'Open': [99, 101, 100, 104, 106, 105, 107, 109, 108, 110],
        'High': [101, 103, 102, 106, 108, 107, 109, 111, 110, 112],
        'Low': [98, 100, 99, 103, 105, 104, 106, 108, 107, 109],
        'Volume': [1000000] * 10
    })
    
    analyzer = TechnicalAnalyzer(sample_data)
    sma = analyzer.calculate_sma(5)
    rsi = analyzer.calculate_rsi(14)
    signals = analyzer.get_trading_signals()
    
    assert len(sma) == 10
    assert len(rsi) == 10
    assert 'rsi' in signals
    
    print(" test_technical_analyzer passed")

if __name__ == "__main__":
    test_analyzer_initialization()
    test_sentiment_analysis()
    test_technical_analyzer()
    print(" All tests passed!")