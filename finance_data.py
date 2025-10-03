import yfinance as yf

def get_stock_data(ticker, period="3mo"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df
