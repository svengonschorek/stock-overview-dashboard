import yfinance as yt
import streamlit as st

def display_financial_metrics(symbol):
    data = yt.Ticker(symbol).quarterly_financials

    results_last_quarter = data[data.columns.values[0]]
    results_last_quarter_prev_year = data[data.columns.values[4]]

    revenue_growth_yoy = (results_last_quarter - results_last_quarter_prev_year) / results_last_quarter_prev_year

    revenue_million = results_last_quarter['Total Revenue'] / 1_000_000
    ebitda_million = results_last_quarter['EBITDA'] / 1_000_000
    ebit_million = results_last_quarter['EBIT'] / 1_000_000

    st.metric(
        label="Total Revenue (Millions USD)",
        value=f"${revenue_million:,.1f}M",
        delta=f"{revenue_growth_yoy['Total Revenue']:.2%} YoY"
    )

    st.metric(
        label="EBITDA (Millions USD)",
        value=f"${ebitda_million:,.1f}M",
        delta=f"{revenue_growth_yoy['EBITDA']:.2%} YoY"
    )

    st.metric(
        label="EBIT (Millions USD)",
        value=f"${ebit_million:,.1f}M",
        delta=f"{revenue_growth_yoy['EBIT']:.2%} YoY"
    )
