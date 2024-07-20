from flask import Blueprint, request, render_template, jsonify
from models import db, Stock
from scraper import fetch_stock_data, fetch_stock_news
from predictor import predict_stock_price, calculate_sma, calculate_ema, calculate_rsi, calculate_macd

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_routes.route('/stock', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return render_template('index.html', error='Ticker symbol is required')

    try:
        # Fetch stock data
        price, market_cap, week_high, week_low, hist = fetch_stock_data(ticker)
        news_content = fetch_stock_news(ticker)
        predicted_price = predict_stock_price(hist)

        # Calculate indicators
        sma = calculate_sma(hist, 14).iloc[-1]
        ema = calculate_ema(hist, 14).iloc[-1]
        rsi = calculate_rsi(hist, 14).iloc[-1]
        macd, macd_signal = calculate_macd(hist)
        macd = macd.iloc[-1]
        macd_signal = macd_signal.iloc[-1]

        # Format historical data
        history_html = hist.to_html(classes='data')

        return render_template('index.html', 
                               ticker=ticker, 
                               price=price, 
                               market_cap=market_cap, 
                               week_high=week_high, 
                               week_low=week_low, 
                               history=history_html, 
                               news=news_content,
                               predicted_price=predicted_price,
                               sma=sma,
                               ema=ema,
                               rsi=rsi,
                               macd=macd,
                               macd_signal=macd_signal)
    except Exception as e:
        return render_template('index.html', error=str(e))

def configure_routes(app):
    app.register_blueprint(main_routes)

