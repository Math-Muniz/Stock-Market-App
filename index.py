import streamlit as st
import investpy as inv
import datetime
import history as hist
import bollinger_bands as bollinger
import styles
import streamlit_toggle as tog
import time

tickers = inv.get_stocks_list("brazil")

st.set_page_config(
    page_title='Stock Exchange',
    page_icon=':bar_chart:',
    layout='wide')

styles.set()

with st.sidebar:
    ticker = st.selectbox(
        'Select the Action or Real Estate Fund',
        tickers,
    )

    date_reference = st.date_input(
        "Select a init of period",
        datetime.datetime.today()
    )

    number_of_days = st.number_input('Insert a number of days', value=30)

    sleep_time = st.select_slider(
        'Select update time (seconds)',
        options=[5, 10, 15, 30, 60]
    )

    init_date = date_reference + datetime.timedelta(days=-(30 + number_of_days))
    end_date = date_reference

    toogle = tog.toggle(
        widget = "radio",
        label = (f"Auto Refresh ({sleep_time}s)"),
        key = "Key1", 
        value =False 
        )

def prepare_history_visualization():
    history, instance = hist.get(ticker, init_date=init_date, end_date=end_date) if init_date else hist.get(ticker)
    if not history.empty:
        print("CURRENT PRICE ->", history["Close"].iat[-1])
    else:
        print('insuficient analisys')
    bollinger_figure = bollinger.get(ticker, history)

    if 'Close' in history.columns and len(history) > 0:
        current_close = history['Close'].iloc[-1]
        previous_close = history['Close'].iloc[-2] if len(history) > 1 else None

        if current_close and previous_close:
            current_value.metric("Current Value", f"R$ {round(current_close, 2)}", f"{round(((current_close / previous_close) - 1) * 100, 2)}%")
        else:
            current_value.metric("Current Value", "N/A", "N/A")

        if 'Close' in history.columns:
            min_value.metric("Minimum Value", f"R$ {round(history['Close'].min(),2)}", f"{round(((history['Close'].min() / current_close) - 1) * 100, 2)}%")
        else:
            min_value.metric("Minimum Value", "N/A", "N/A")
        
        if 'Close' in history.columns:
            max_value.metric("Maximum Value", f"R$ {round(history['Close'].max(),2)}", f"{round(((history['Close'].min() / current_close) - 1) * 100, 2)}%")
        else:
            max_value.metric("Maximum Value", "N/A", "N/A")
    else:
        current_value.metric("Current Value", "N/A", "N/A")
        min_value.metric("Minimum Value", "N/A", "N/A")
        max_value.metric("Maximum Value", "N/A", "N/A")

    graph.plotly_chart(bollinger_figure, use_container_width=True, sharing="streamlit")

if ticker and sleep_time:

    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_value = st.empty()
    with col2:
        min_value = st.empty()
    with col3:
        max_value = st.empty()
    graph = st.empty()

    while toogle:
        prepare_history_visualization()
        time.sleep(sleep_time)
    else:
        prepare_history_visualization()
