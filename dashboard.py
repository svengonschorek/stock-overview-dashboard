import streamlit as st

from components.chart_candlestick import load_candlestick
from components.main_sidebar import sidebar_company_info
from components.financials_waterfall import load_waterfall
from components.financials_metrics import display_financial_metrics
from components.stocks_totallist import stocks_list

st.set_page_config(layout="wide", page_title="Company Analysis Dashboard")

# load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Stock list popup
@st.dialog("Stocks List", width='large')
def stocks_list_popup():
    stocks_list()

# Popup buttons
button_col1, button_col2, _ = st.columns([1, 1, 7])
with button_col1:
    st.button("Stocks List", on_click=stocks_list_popup)
with button_col2:
    st.button("Watchlist")

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

    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("Metrics")
        display_financial_metrics(symbol)
    with col2:
        st.plotly_chart(st.session_state.waterfall_chart, use_container_width=True)
