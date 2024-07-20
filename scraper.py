import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from models import db, Stock
from datetime import datetime
import pandas as pd
import time

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch current price
    price = stock.history(period='1d')['Close'].iloc[-1]
    
    # Fetch stock info for market cap, 52-week high, and 52-week low
    info = stock.info
    market_cap = info.get('marketCap', 'N/A')
    week_high = info.get('fiftyTwoWeekHigh', 'N/A')
    week_low = info.get('fiftyTwoWeekLow', 'N/A')

    # Fetch historical data for the last 5 days
    hist = stock.history(period='5d')
    
    return price, market_cap, week_high, week_low, hist

def fetch_stock_news(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/news'
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(5)
        
        news_elements = driver.find_elements(By.CSS_SELECTOR, 'div.Cf')
        news_content = "\n\n".join([elem.text for elem in news_elements if elem.text])
        
        return news_content if news_content else "No news available"
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to fetch news"
    finally:
        driver.quit()

