import requests
from bs4 import BeautifulSoup

def get_stock_news(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = [h.get_text() for h in soup.find_all('h3')]
    return headlines[:10]
