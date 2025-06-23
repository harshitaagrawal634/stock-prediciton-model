# stock-prediciton-model
An interactive web application that helps users analyze and forecast stock prices using real-world financial data and time series modeling.

Built with **Streamlit**, the app combines rich data visualization, predictive modeling, and real-time market insights into one seamless user experience.

---

## Features

- **Stock Analysis Dashboard**
  - View company summary, sector, key financial metrics
  - Visualize historical stock performance
  - Interactive charts: Candlestick, Line Charts with RSI, MACD, and Moving Averages

- **Stock Price Prediction**
  - Forecast closing prices for the next 30 days
  - Time series modeling using ARIMA with rolling average smoothing and differencing
  - Model evaluation via RMSE
  - Interactive forecast visualizations using Plotly

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend / Modeling**: ARIMA (from `statsmodels`)
- **Data Source**: Yahoo Finance API via `yfinance`
- **Visualization**: Plotly, pandas-ta (for indicators)
- **Libraries**: NumPy, pandas, scikit-learn, statsmodels

---

## How It Works

### Stock Analysis

- User enters a stock ticker (e.g., AAPL)
- App fetches latest data using `yfinance`
- Displays:
  - Company info (sector, employees, website)
  - Key financial ratios (P/E, EPS, ROE, etc.)
  - Recent price movements
  - Technical indicators like RSI, MACD, and SMA

### Stock Prediction

- ARIMA model is used to forecast future prices
- Includes preprocessing: rolling mean, stationarity check (ADF test), and scaling
- Forecast for the next 30 days is generated and visualized
- RMSE score displayed for model accuracy