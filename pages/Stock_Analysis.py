import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta

from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import filter_data
from pages.utils.plotly_figure import close_chart
from pages.utils.plotly_figure import candlestick
from pages.utils.plotly_figure import RSI
from pages.utils.plotly_figure import Moving_average
from pages.utils.plotly_figure import MACD

st.set_page_config(
    page_title="Stock Analysis",
    page_icon=":page_with_curl:",
    layout="wide",
)

st.title("Stock Analysis")

col1,col2,col3= st.columns(3)

today= datetime.date.today()

with col1:
    ticker=st.text_input("Stock Ticker", "AAPL")
with col2:
    start_date= st.date_input("Choose Start Date", datetime.date(today.year-1, today.month,today.day))
with col3:
    end_date=st.date_input("Choose End Date",today)

st.subheader(ticker)

stock = yf.Ticker(ticker)

try:
    info = stock.info
except Exception as e:
    info = {}
    st.warning(f"Could not fetch stock info: {e}")

st.write(info.get('longBusinessSummary', 'No summary available.'))
st.write("**Sector:**", info.get('sector', 'N/A'))
st.write("**Full Time Employees:**", info.get('fullTimeEmployees', 'N/A'))
st.write("**Website:**", info.get('website', 'N/A'))

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=['Market cap', 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [
        info.get("marketCap", "N/A"),
        info.get("beta", "N/A"),
        info.get("trailingEps", "N/A"),
        info.get("trailingPE", "N/A"),
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
    df[''] = [
        info.get("quickRatio", "N/A"),
        info.get("revenuePerShare", "N/A"),
        info.get("profitMargins", "N/A"),
        info.get("debtToEquity", "N/A"),
        info.get("returnOnEquity", "N/A"),
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1])

num_period= ''
with col1:
    if st.button('5D'):
        num_period='5d'
with col2:
    if st.button('1M'):
        num_period='1mo'
with col3:
    if st.button('6M'):
        num_period='6mo'
with col4:
    if st.button('YTD'):
        num_period='ytd'
with col5:
    if st.button('1Y'):
        num_period='1y'
with col6:
    if st.button('5Y'):
        num_period='5y'
with col7:
    if st.button('MAX'):
        num_period='max'

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    chart_type = st.selectbox('', ('Candle', 'Line'))

with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period = 'max')
data1 = ticker_.history(period = 'max')

if num_period == "":
    
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
else:

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(new_df1, num_period), use_container_width=True)
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

    
