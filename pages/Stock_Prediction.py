from ast import And
from tracemalloc import start
import streamlit as st
from pages.utils.model_train import get_rolling_mean, get_differencing_order, get_stock_data, scaling, evaluate_model, get_forecast, inverse_scaling
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Stock Prediciton",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

st.title("Stock Prediciton")

col1,col2,col3=st.columns(3)

with col1:
    ticker= st.text_input('Stock Ticker','AAPL')

rmse=0

st.subheader('Predicting Next 30 days Close price for: '+ticker)

start = datetime.now() - timedelta(days=365*15)  # 15 years ago
end = datetime.now()

close_price= get_stock_data(ticker, start, end)
rolling_price= get_rolling_mean(close_price)
differencing_order= get_differencing_order(rolling_price)
scaled_data, scaler= scaling(rolling_price)

rmse= evaluate_model(scaled_data,differencing_order)

st.write("**Model RMSE Score:**",rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
st.write('##### Forecast Data (Next 30 days)')
fig_tail= plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height = 220)
st.plotly_chart(fig_tail, use_container_width=True)

forecast = pd.concat([rolling_price, forecast])

st.plotly_chart(Moving_average_forecast(forecast),use_container_width= True)
