# Stock-Trend-Visualizer-News-Sentiment-Analyzer

A simple yet powerful Streamlit web app that helps layman investors analyze stock trends and understand the market mood from news articles.
The app combines historical price visualization 📊 and news sentiment analysis 📰 to give an easy-to-understand traffic-light Buy/Sell signal 🚦.


Features

🔍 Search any stock by ticker symbol (e.g., AAPL, TSLA, TCS.NS)

<img width="1848" height="276" alt="image" src="https://github.com/user-attachments/assets/68cddb0c-6119-4b82-a26e-a08a3b8c614e" />


📉 Visualize stock price trends (last 6 months) with a clean graph

<img width="1710" height="891" alt="image" src="https://github.com/user-attachments/assets/f44cee19-f483-40f0-9725-ee8cea7454ce" />

📰 Fetch latest news headlines about the company
😊 Analyze positive / neutral / negative sentiment from the news
🚦 Traffic-Light Indicator:
🟢 Buy (positive news + uptrend)
🔴 Sell (negative news + downtrend)
🟡 Hold (mixed signals)
💰 “If you had invested ₹10,000 last year…” simulator

<img width="988" height="806" alt="image" src="https://github.com/user-attachments/assets/6ff9d905-fba5-4034-9c14-6579f38dc18a" />



Tech Stack

Frontend: Streamlit
Backend: Python
Data Sources: yfinance → stock data
NLTK VADER → sentiment analysis
Visualization: Matplotlib

