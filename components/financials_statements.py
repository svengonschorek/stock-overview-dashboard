import yfinance as yf
import streamlit as st

def financials_statements(symbol):
    data = yf.Ticker(symbol)
    balance_sheet = data.quarterly_balance_sheet
    income_statement = data.quarterly_financials
    cash_flow = data.quarterly_cashflow

    st.subheader("Income Statement")
    st.dataframe(income_statement)

    st.subheader("Balance Sheet")
    st.dataframe(balance_sheet)

    st.subheader("Cash Flow Statement")
    st.dataframe(cash_flow)
