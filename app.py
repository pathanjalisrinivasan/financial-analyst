import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from textblob import TextBlob
from time import sleep

# Function to fetch stock symbols based on user input
def fetch_stock_symbols(api_key, keyword):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data.get('bestMatches', [])

# Function to fetch stock data
def fetch_stock_data(api_key, symbol, function='TIME_SERIES_DAILY', outputsize='full'):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}&outputsize={outputsize}'
    response = requests.get(url)
    data = response.json()
    return data

# Function to calculate technical indicators
def calculate_indicators(data):
    df = pd.DataFrame(data['Time Series (Daily)']).T.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Calculate indicators
    df['SMA_20'] = df['4. close'].rolling(window=20).mean()
    df['SMA_50'] = df['4. close'].rolling(window=50).mean()
    df['SMA_200'] = df['4. close'].rolling(window=200).mean()
    
    delta = df['4. close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    df['EMA_12'] = df['4. close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['4. close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

# Function for ARIMA prediction
def arima_prediction(data):
    df = pd.DataFrame(data['Time Series (Daily)']).T.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    model = ARIMA(df['4. close'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)  # Predict next 5 days
    return forecast

# Function for sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Streamlit app
st.title("Indian Stock Market Analysis")

# Sidebar for stock search and API Key
st.sidebar.header("Stock Search and Settings")
api_key = st.sidebar.text_input("Enter your Alpha Vantage API Key:")
keyword = st.sidebar.text_input("Search for a stock:")
selected_stock = None
if keyword and api_key:
    matches = fetch_stock_symbols(api_key, keyword)
    symbols = [match['1. symbol'] for match in matches]
    selected_stock = st.sidebar.selectbox("Select Stock Symbol:", symbols)

# Duration selection
duration = st.sidebar.selectbox("Select Duration:", ['1 day', '1 week', '1 month', '6 months', '1 year'])

if st.sidebar.button("Fetch Data"):
    if api_key and selected_stock:
        with st.spinner("Loading data..."):
            sleep(2)  # Simulate loading time
            data = fetch_stock_data(api_key, selected_stock)
        
        if 'Time Series (Daily)' in data:
            st.success("Data fetched successfully!")

            # Calculate indicators
            indicators = calculate_indicators(data)

            # Create side-by-side graphs
            col1, col2 = st.columns(2)

            with col1:
                # SMA line chart
                st.subheader("Technical Indicators (SMA)")
                st.line_chart(indicators[['SMA_20', 'SMA_50', 'SMA_200']])

            with col2:
                # Candlestick chart
                st.subheader("Candlestick Chart")
                fig = go.Figure(data=[go.Candlestick(x=indicators.index,
                                                      open=indicators['1. open'],
                                                      high=indicators['2. high'],
                                                      low=indicators['3. low'],
                                                      close=indicators['4. close'])])
                fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
                st.plotly_chart(fig)

            # Next set of graphs
            col3, col4 = st.columns(2)

            with col3:
                st.subheader("RSI")
                st.line_chart(indicators['RSI'])

            with col4:
                st.subheader("MACD")
                st.line_chart(indicators[['MACD', 'Signal_Line']])

            # Predict future prices using ARIMA
            predicted_prices = arima_prediction(data)
            st.subheader("ARIMA Price Prediction for Next 5 Days")
            st.write(predicted_prices)

            # Sentiment analysis
            news_article = "Market is bullish today due to positive earnings reports."  # Example news text
            sentiment_score = analyze_sentiment(news_article)
            st.subheader("Market News Sentiment Analysis")
            st.write(f"Sentiment Score: {sentiment_score:.2f}")

            # Automated Insights
            st.subheader("Automated Insights")
            insights = []
            if indicators['4. close'][-1] > indicators['SMA_50'][-1]:
                insights.append("Current price is above the 50-day SMA, indicating an upward trend.")
            else:
                insights.append("Current price is below the 50-day SMA, indicating a downward trend.")

            if indicators['RSI'][-1] < 30:
                insights.append("RSI indicates the stock may be oversold.")
            elif indicators['RSI'][-1] > 70:
                insights.append("RSI indicates the stock may be overbought.")

            st.write("\n".join(insights))

            # Recommendation System
            st.subheader("Stock Recommendation")
            if sentiment_score > 0.1 and indicators['4. close'][-1] > indicators['SMA_50'][-1]:
                st.write(f"We recommend buying {selected_stock} based on positive sentiment and upward trend.")
            else:
                st.write(f"We advise caution with {selected_stock} as sentiment is low or trends are not favorable.")
        else:
            st.error("Error fetching data. Please check the stock symbol or API key.")
    else:
        st.warning("Please enter your API key and select a stock symbol.")