import streamlit as st

from components.chart_candlestick import load_candlestick
from components.main_sidebar import sidebar_company_info
from components.financials_waterfall import load_waterfall

st.set_page_config(layout="wide")

#st.title("Company Stock Dashboard")

# load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
symbol = st.sidebar.text_input("Symbol", "AAPL").upper()
sidebar_company_info(symbol)

# Tabs
chart_tab, financial_tab = st.tabs(["Chart", "Financial"])

with chart_tab:
    st.session_state.candlestick_chart = load_candlestick(symbol)
    st.write(st.session_state.candlestick_chart)

with financial_tab:
    st.session_state.waterfall_chart = load_waterfall(symbol)
    st.write(st.session_state.waterfall_chart)
