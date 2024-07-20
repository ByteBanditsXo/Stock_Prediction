import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_stock_price(hist):
    hist['Date'] = pd.to_datetime(hist.index)
    hist['Date'] = hist['Date'].map(pd.Timestamp.toordinal)
    X = hist[['Date']].values
    y = hist['Close'].values

    # Use the last 5 days to train the model
    X_train = X[-5:]
    y_train = y[-5:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict the next day
    next_day = np.array([[X[-1][0] + 1]])
    predicted_price = model.predict(next_day)[0]

    return predicted_price

def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = calculate_ema(data, short_window)
    long_ema = calculate_ema(data, long_window)
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

