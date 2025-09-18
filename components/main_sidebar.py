import streamlit as st
import yfinance as yf

@st.dialog("Company Info")
def company_info_popup(summary):
    st.write("### Business Summary")
    st.write(summary)
    
def sidebar_company_info(symbol):
    data = yf.Ticker(symbol)
    st.sidebar.title(data.info['longName'])
    st.sidebar.subheader(f"{data.info['fullExchangeName']}: {data.info['symbol']}")
    st.sidebar.write(data.info['website'])
    st.sidebar.write(data.info['sector'], ', ', data.info['industry'])

    st.sidebar.subheader("Summary")
    summary = data.info['longBusinessSummary']
    short_summary = summary[:220] + "..." if len(summary) > 220 else summary
    st.sidebar.write(short_summary)

    st.sidebar.button("More Info", on_click=lambda: company_info_popup(summary))