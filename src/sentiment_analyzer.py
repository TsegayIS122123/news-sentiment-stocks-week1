"""
Sentiment analysis utilities for financial headlines.
"""

from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyze sentiment of financial headline using TextBlob.
    
    Returns:
        float: Polarity score between -1 (negative) and 1 (positive)
    """
    if not isinstance(text, str):
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

if __name__ == "__main__":
    test_text = "Stocks hit record high amid strong earnings"
    score = analyze_sentiment(test_text)
    print(f"Test: '{test_text}' -> Score: {score:.3f} -> {get_sentiment_label(score)}")
