import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockAnalyzer:
    def __init__(self):
        pass
    
    def fetch_stock_data(self, ticker, period="1mo"):
        """Fetch stock data using yfinance"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if hist.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            return hist
        except Exception as e:
            raise Exception(f"Error fetching stock data: {str(e)}")
    
    def calculate_metrics(self, data):
        """Calculate key financial metrics"""
        metrics = {
            'current_price': round(data['Close'][-1], 2),
            'start_price': round(data['Close'][0], 2),
            'price_change': round(data['Close'][-1] - data['Close'][0], 2),
            'price_change_pct': round(((data['Close'][-1] - data['Close'][0]) / data['Close'][0]) * 100, 2),
            'high': round(data['High'].max(), 2),
            'low': round(data['Low'].min(), 2),
            'avg_volume': int(data['Volume'].mean()),
            'volatility': round(data['Close'].pct_change().std() * 100, 2),
            'rsi': self.calculate_rsi(data['Close'])[-1],
            'ma20': round(data['Close'].rolling(window=20).mean().iloc[-1], 2),
            'ma50': round(data['Close'].rolling(window=50).mean().iloc[-1], 2) if len(data) >= 50 else None,
        }
        return metrics
    
    def calculate_rsi(self, prices, periods=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    
    def generate_analysis(self, metrics, data):
        """Generate technical analysis insights"""
        analysis = []
        
        # Trend Analysis
        if metrics['price_change'] > 0:
            trend = "upward"
        else:
            trend = "downward"
            
        analysis.append(f"📈 Trend Analysis:")
        analysis.append(f"- The stock has shown a {trend} trend with a {metrics['price_change_pct']}% change")
        analysis.append(f"- Price moved from ${metrics['start_price']} to ${metrics['current_price']}")
        
        # Volume Analysis
        avg_volume = metrics['avg_volume']
        recent_volume = data['Volume'][-5:].mean()
        volume_change = ((recent_volume - avg_volume) / avg_volume) * 100
        
        analysis.append(f"\n📊 Volume Analysis:")
        analysis.append(f"- Average daily volume: {avg_volume:,.0f} shares")
        analysis.append(f"- Recent volume is {abs(round(volume_change, 2))}% {'higher' if volume_change > 0 else 'lower'} than average")
        
        # Technical Indicators
        analysis.append(f"\n🔍 Technical Indicators:")
        analysis.append(f"- RSI (14): {metrics['rsi']} ({'Oversold' if metrics['rsi'] < 30 else 'Overbought' if metrics['rsi'] > 70 else 'Neutral'})")
        analysis.append(f"- 20-day MA: ${metrics['ma20']}")
        if metrics['ma50']:
            analysis.append(f"- 50-day MA: ${metrics['ma50']}")
        
        # Volatility
        analysis.append(f"\n📉 Volatility Analysis:")
        analysis.append(f"- 30-day volatility: {metrics['volatility']}%")
        analysis.append(f"- Trading range: ${metrics['low']} - ${metrics['high']}")
        
        return "\n".join(analysis)

def main():
    st.set_page_config(page_title="Stock Analysis Platform", layout="wide")
    
    st.title("📊 Stock Analysis Platform")
    st.write("Real-time technical analysis and market insights")
    
    # Sidebar
    with st.sidebar:
        st.header("Analysis Settings")
        period = st.selectbox(
            "Analysis Period",
            ["1mo", "3mo", "6mo", "1y"],
            index=0
        )
        
        st.markdown("""
        ### About
        This tool provides:
        - Real-time stock data
        - Technical analysis
        - Key market metrics
        - Price trends and patterns
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("Stock Input")
        ticker = st.text_input("Enter Stock Ticker:", "AAPL").upper()
        analyze_button = st.button("📊 Analyze Stock")
    
    if analyze_button:
        with st.spinner("Analyzing stock data..."):
            try:
                analyzer = StockAnalyzer()
                data = analyzer.fetch_stock_data(ticker, period)
                metrics = analyzer.calculate_metrics(data)
                analysis = analyzer.generate_analysis(metrics, data)
                
                # Display stock chart
                with col1:
                    st.subheader(f"{ticker} Stock Price")
                    st.line_chart(data['Close'])
                    
                    st.subheader("Trading Volume")
                    st.bar_chart(data['Volume'])
                
                # Display metrics
                st.subheader("Key Metrics")
                col3, col4, col5, col6 = st.columns(4)
                with col3:
                    st.metric("Current Price", f"${metrics['current_price']}")
                with col4:
                    st.metric("Price Change", 
                             f"${metrics['price_change']}", 
                             f"{metrics['price_change_pct']}%")
                with col5:
                    st.metric("RSI", f"{metrics['rsi']}")
                with col6:
                    st.metric("Volatility", f"{metrics['volatility']}%")
                
                # Display analysis
                st.subheader("Technical Analysis")
                st.markdown(analysis)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure the ticker symbol is valid")

if __name__ == "__main__":
    main()