"""
Analysis Engine - Lightweight OOP implementation for financial analysis
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

class FinancialNewsAnalyzer:
    """OOP class for financial news sentiment analysis"""
    
    def __init__(self, news_data=None, stock_data=None):
        self.news_data = news_data
        self.stock_data = stock_data
        self.merged_data = None
        self.correlation_results = {}
        
    def load_news_data(self, filepath):
        """Load and preprocess news data"""
        self.news_data = pd.read_csv(filepath)
        self.news_data['date'] = pd.to_datetime(self.news_data['date'], format='mixed', utc=True)
        self.news_data['date_only'] = self.news_data['date'].dt.date
        return self.news_data
    
    def load_stock_data(self, symbol, data_dir):
        """Load and preprocess stock data"""
        filepath = f"{data_dir}/{symbol}.csv"
        self.stock_data = pd.read_csv(filepath)
        self.stock_data['Date'] = pd.to_datetime(self.stock_data['Date'])
        self.stock_data['date_only'] = self.stock_data['Date'].dt.date
        self.stock_data['daily_return'] = self.stock_data['Close'].pct_change()
        return self.stock_data
    
    def analyze_sentiment(self, text):
        """Analyze sentiment with comprehensive error handling"""
        if not isinstance(text, str) or pd.isna(text):
            return 0.0
        try:
            return TextBlob(text).sentiment.polarity
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 0.0
    
    def calculate_daily_sentiment(self):
        """Calculate daily aggregated sentiment"""
        if self.news_data is None:
            raise ValueError("News data not loaded")
        
        self.news_data['sentiment_score'] = self.news_data['headline'].apply(self.analyze_sentiment)
        
        daily_sentiment = self.news_data.groupby('date_only').agg({
            'sentiment_score': ['mean', 'std', 'count']
        }).round(4)
        
        daily_sentiment.columns = ['sentiment_mean', 'sentiment_std', 'article_count']
        return daily_sentiment.reset_index()
    
    def merge_datasets(self, symbol='AAPL'):
        """Merge news and stock data with alignment"""
        daily_sentiment = self.calculate_daily_sentiment()
        
        # Filter for specific stock
        stock_news = self.news_data[self.news_data['stock'] == symbol]
        daily_sentiment_stock = stock_news.groupby('date_only').agg({
            'sentiment_score': ['mean', 'std', 'count']
        }).round(4)
        daily_sentiment_stock.columns = ['sentiment_mean', 'sentiment_std', 'article_count']
        
        # Merge with stock data
        self.merged_data = pd.merge(
            daily_sentiment_stock.reset_index(),
            self.stock_data[['date_only', 'Close', 'daily_return']],
            on='date_only',
            how='inner'
        )
        return self.merged_data
    
    def calculate_correlations(self):
        """Calculate comprehensive correlation analysis"""
        if self.merged_data is None:
            self.merge_datasets()
        
        # Pearson correlation
        pearson_corr, pearson_p = pearsonr(
            self.merged_data['sentiment_mean'].dropna(),
            self.merged_data['daily_return'].dropna()
        )
        
        # Spearman correlation
        spearman_corr, spearman_p = spearmanr(
            self.merged_data['sentiment_mean'].dropna(),
            self.merged_data['daily_return'].dropna()
        )
        
        self.correlation_results = {
            'pearson': {'correlation': pearson_corr, 'p_value': pearson_p},
            'spearman': {'correlation': spearman_corr, 'p_value': spearman_p},
            'sample_size': len(self.merged_data),
            'date_range': f"{self.merged_data['date_only'].min()} to {self.merged_data['date_only'].max()}"
        }
        
        return self.correlation_results
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        if not self.correlation_results:
            self.calculate_correlations()
        
        report = {
            'correlation_summary': self.correlation_results,
            'sentiment_stats': self.merged_data['sentiment_mean'].describe(),
            'return_stats': self.merged_data['daily_return'].describe(),
            'data_quality': {
                'merged_records': len(self.merged_data),
                'news_articles': len(self.news_data),
                'stock_days': len(self.stock_data)
            }
        }
        return report

class TechnicalAnalyzer:
    """OOP class for technical analysis"""
    
    def __init__(self, stock_data):
        self.stock_data = stock_data
        self.indicators = {}
    
    def calculate_sma(self, window=20):
        """Calculate Simple Moving Average"""
        self.indicators[f'SMA_{window}'] = self.stock_data['Close'].rolling(window=window).mean()
        return self.indicators[f'SMA_{window}']
    
    def calculate_rsi(self, window=14):
        """Calculate Relative Strength Index"""
        delta = self.stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        self.indicators['RSI'] = 100 - (100 / (1 + rs))
        return self.indicators['RSI']
    
    def get_trading_signals(self):
        """Generate trading signals based on technical indicators"""
        signals = {}
        
        if 'RSI' in self.indicators:
            current_rsi = self.indicators['RSI'].iloc[-1]
            if current_rsi < 30:
                signals['rsi'] = 'OVERSOLD'
            elif current_rsi > 70:
                signals['rsi'] = 'OVERBOUGHT'
            else:
                signals['rsi'] = 'NEUTRAL'
        
        return signals