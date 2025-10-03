from textblob import TextBlob

def analyze_sentiment(headlines):
    results = []
    for h in headlines:
        polarity = TextBlob(h).sentiment.polarity
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        results.append((h, sentiment))
    return results
