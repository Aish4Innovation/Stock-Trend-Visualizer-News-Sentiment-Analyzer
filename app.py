# import streamlit as st
# import yfinance as yf
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from textblob import TextBlob
# from yahoo_fin import news

# # --- Helper Functions ---

# # Fetch stock price data
# def get_stock_data(ticker, period="1mo", interval="1d"):
#     stock = yf.Ticker(ticker)
#     return stock.history(period=period, interval=interval)

# # Sentiment analysis
# def analyze_sentiment(text):
#     analysis = TextBlob(text)
#     if analysis.sentiment.polarity > 0:
#         return "Positive"
#     elif analysis.sentiment.polarity < 0:
#         return "Negative"
#     else:
#         return "Neutral"


# # --- Streamlit App ---
# st.set_page_config(page_title="Stock Trend + Sentiment Analyzer", layout="wide")

# st.title("📈 Stock Trend Visualizer + 📰 Sentiment Analyzer")

# # Input stock symbol
# stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, MSFT):", "AAPL")

# # Dropdown for period selection
# period = st.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=0)

# if stock_symbol:
#     # --- Stock Data ---
#     st.subheader(f"Stock Price Trend for {stock_symbol} ({period})")
#     data = get_stock_data(stock_symbol, period=period)

#     if not data.empty:
#         fig, ax = plt.subplots(figsize=(10, 5))
#         ax.plot(data.index, data['Close'], label="Close Price", color="blue")

#         # Format date axis
#         ax.xaxis.set_major_locator(mdates.AutoDateLocator())
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
#         fig.autofmt_xdate()

#         ax.set_xlabel("Date")
#         ax.set_ylabel("Price (USD)")
#         ax.set_title(f"{stock_symbol} Closing Price Trend")
#         ax.legend()
#         st.pyplot(fig)
#     else:
#         st.warning("No stock data found. Please check the symbol or period.")

#     # --- Latest News ---
#     st.subheader(f"Latest News for {stock_symbol}")
#     try:
#         stock_news = news.get_yf_rss(stock_symbol)
#         if stock_news:
#             for i, article in enumerate(stock_news[:5]):  # show top 5 news
#                 title = article["title"]
#                 link = article["link"]
#                 sentiment = analyze_sentiment(title)
#                 st.markdown(f"- [{title}]({link}) → **{sentiment}**")
#         else:
#             st.info("No recent news found for this stock.")
#     except Exception as e:
#         st.error(f"Error fetching news: {e}")

import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from textblob import TextBlob
from yahoo_fin import news

st.set_page_config(page_title="Stock Trend + Sentiment Analyzer", layout="wide")

st.title("📈 Stock Trend Visualizer + Sentiment Analyzer")

# User input
stock_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, INFY.NS)", "AAPL")

# Fetch stock data
def fetch_stock_data(symbol):
    try:
        data = yf.download(symbol, period="1y", interval="1d")
        return data
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return pd.DataFrame()

# Sentiment analysis
def analyze_sentiment(news_list):
    sentiments = []
    for article in news_list:
        title = article["title"]
        analysis = TextBlob(title)
        sentiments.append(analysis.sentiment.polarity)
    if sentiments:
        return np.mean(sentiments)
    return 0

# Traffic light indicator
def traffic_light_indicator(symbol, avg_sentiment):
    try:
        data = yf.download(symbol, period="6mo", interval="1d")["Close"]
        if data.empty:
            return "⚠️ No stock data available"
    except Exception as e:
        return f"⚠️ Error fetching stock data: {e}"

    if len(data) > 10:
        x = np.arange(len(data[-10:]))
        y = data[-10:]
        slope, _ = np.polyfit(x, y, 1)
    else:
        slope = 0

    if slope > 0 and avg_sentiment > 0.1:
        return "🟢 Strong Buy Signal"
    elif slope < 0 and avg_sentiment < -0.1:
        return "🔴 Strong Sell Signal"
    else:
        return "🟡 Hold / Neutral"

# Investment calculator
def investment_return(symbol):
    try:
        data = yf.download(symbol, period="1y", interval="1d")
        if data.empty or "Close" not in data:
            return "⚠️ Not enough data"

        # Handle both Series & DataFrame
        close_prices = data["Close"]
        if isinstance(close_prices, pd.DataFrame):
            close_prices = close_prices.iloc[:, 0]  # Take the first column

        first_price = close_prices.iloc[0]
        last_price = close_prices.iloc[-1]

        growth = (last_price / first_price) * 10000
        return f"If you had invested ₹10,000 last year, it would be worth ₹{growth:,.2f} today."
    except Exception as e:
        return f"⚠️ Error calculating return: {e}"

# Display stock graph
stock_data = fetch_stock_data(stock_symbol)
if not stock_data.empty:
    st.subheader(f"Stock Price Trend for {stock_symbol}")
    fig, ax = plt.subplots(figsize=(5, 2), dpi=100) 
    ax.plot(stock_data.index, stock_data["Close"], label="Close Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    st.pyplot(fig)

# News
st.subheader(f"Latest News for {stock_symbol}")
try:
    news_list = news.get_yf_rss(stock_symbol)
    if news_list:
        for article in news_list[:5]:
            st.write(f"📰 [{article['title']}]({article['link']})")
    else:
        st.write("No news found.")
except Exception as e:
    st.error(f"Error fetching news: {e}")
    news_list = []

# Sentiment
avg_sentiment = analyze_sentiment(news_list) if news_list else 0
st.subheader("🧠 News Sentiment Analysis")
st.write(f"Average Sentiment Score: {avg_sentiment:.2f}")

# Traffic Light Indicator
st.subheader("🚦 Traffic-Light Buy/Sell Indicator")
st.write(traffic_light_indicator(stock_symbol, avg_sentiment))

# Investment Return
st.subheader("💰 Investment Insight")
st.write(investment_return(stock_symbol))
