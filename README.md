# Indian Stock Market Analysis App

This repository contains a Streamlit application for analyzing stock market data using the Alpha Vantage API. The app allows users to search for stocks, view technical indicators, and receive insights and recommendations based on sentiment analysis.

## Features

* Technical Indicators: Displays Simple Moving Averages (SMA), Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD).
* Candlestick Charts: Visual representation of stock price movements.
* Sentiment Analysis: Analyzes market sentiment based on news articles (**Note: Implement sentiment analysis functionality if included**).
* Automated Insights: Provides insights based on technical indicators (**Note: Implement automated insights functionality if included**).
* Stock Recommendations: Suggests whether to buy the stock based on sentiment and trends (**Note: Implement stock recommendations functionality if included**).

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Python 3.6 or higher
* An active Alpha Vantage API key (you can get one for free at Alpha Vantage)

## Installation

Follow these steps to set up the application:

1. **Clone the Repository:**

   Open your terminal and run the following command to clone the repository:

   ```bash
   git clone https://github.com/pathanjalisrinivasan/stock-analyst.git
   cd stock-analyst
   ```
   
Create a Virtual Environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Install Required Libraries:

```bash
pip install streamlit pandas numpy requests plotly statsmodels textblob
```

## Running the Application
Navigate to the directory where the app is located and run:

```bash
streamlit run app.py
```

## Access the Application:

Open your web browser and go to http://localhost:8501 to access the application.

## Input Your Alpha Vantage API Key:

On the sidebar, enter your Alpha Vantage API key.

## Search for a Stock:

Use the search box to find a stock by its symbol.

## View the Analysis:

Click on "Fetch Data" to view the technical indicators, candlestick charts, RSI, MACD, sentiment analysis, automated insights, and stock recommendations.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.
