"""
Sentiment analysis utilities
"""

from textblob import TextBlob

def analyze_sentiment(text):
    """Analyze sentiment of financial headline using TextBlob."""
    if not isinstance(text, str) or pd.isna(text):
        return 0.0
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def get_sentiment_label(score):
    """Convert sentiment score to label"""
    if score > 0.1:
        return 'positive'
    elif score < -0.1:
        return 'negative'
    else:
        return 'neutral'