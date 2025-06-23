import streamlit as st

st.set_page_config(
    page_title="Trading App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

st.title("Trading Guide App :bar_chart:")

st.header("We provide the Greatest platform for you to collect all information prior to investing in stocks.")

st.image("photo.jpg")

st.markdown("## We provide the following services:")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all the information about stock.")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models. Use it as an insight, not a guarantee.")
