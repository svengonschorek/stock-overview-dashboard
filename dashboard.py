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

# Sidebar with default symbol from query parameter
query_symbol = None
if hasattr(st, "query_params"):
    query_symbol = st.query_params.get("symbol", None)

default_symbol = query_symbol.upper() if query_symbol else "AAPL"

symbol = st.sidebar.text_input("Symbol", default_symbol).upper()
st.sidebar.button("Stocks", on_click=stocks_list_popup)
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
