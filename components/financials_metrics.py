import yfinance as yt
import streamlit as st

data = yt.Ticker("GOOGL").quarterly_financials

print(data)

results_last_quarter = data[data.columns.values[0]]
results_last_quarter_prev_year = data[data.columns.values[4]]
revenue_growth_yoy = (results_last_quarter - results_last_quarter_prev_year) / results_last_quarter_prev_year

print(results_last_quarter)
print(revenue_growth_yoy)
