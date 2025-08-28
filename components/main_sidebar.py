import streamlit as st
import yfinance as yf
from datetime import datetime

def sidebar_company_info(symbol):
    data = yf.Ticker(symbol)
    st.sidebar.title(data.info['longName'])
    st.sidebar.subheader(f"{data.info['fullExchangeName']}: {data.info['symbol']}")
    st.sidebar.write(data.info['website'])
    st.sidebar.write(data.info['sector'], ', ', data.info['industry'])
    st.sidebar.subheader("Most recent quarter")
    st.sidebar.write(datetime.fromtimestamp(data.info['mostRecentQuarter']).strftime('%Y-%m-%d %H:%M:%S'))
    st.sidebar.subheader("Next Earnings Call")
    st.sidebar.write(datetime.fromtimestamp(data.info['earningsTimestampStart']).strftime('%Y-%m-%d %H:%M:%S'))
