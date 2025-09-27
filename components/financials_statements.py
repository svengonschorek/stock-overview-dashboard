import pandas as pd
import yfinance as yf
import streamlit as st

def financials_statements(symbol):
    data = yf.Ticker(symbol)
    balance_sheet = data.quarterly_balance_sheet
    income_statement = data.quarterly_financials
    cash_flow = data.quarterly_cashflow

    # Convert the date column from timestamp to date
    income_statement.columns = [col.date() if hasattr(col, "date") else col for col in income_statement.columns]
    balance_sheet.columns = [col.date() if hasattr(col, "date") else col for col in balance_sheet.columns]
    cash_flow.columns = [col.date() if hasattr(col, "date") else col for col in cash_flow.columns]

     # Rows to exclude from conversion
    exclude_rows = ["Tax Rate For Calcs", "Diluted EPS", "Basic EPS"]

    # Convert values to millions except for excluded rows
    def convert_to_millions_and_format(df):
        df_million = df.copy().astype(object)  # Cast all columns to object dtype
        for row in df_million.index:
            if row not in exclude_rows:
                df_million.loc[row] = df_million.loc[row].apply(lambda x: f"${int(round(x / 1_000_000)):,}M" if pd.notnull(x) else "")
            else:
                df_million.loc[row] = df_million.loc[row].apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
        return df_million

    income_statement_million = convert_to_millions_and_format(income_statement)
    balance_sheet_million = convert_to_millions_and_format(balance_sheet)
    cash_flow_million = convert_to_millions_and_format(cash_flow)

    st.subheader("Income Statement")
    st.table(
        data=income_statement_million.iloc[:, :5],
        border="horizontal"
    )

    st.subheader("Balance Sheet")
    st.table(
        data=balance_sheet_million.iloc[:, :5],
        border="horizontal"
    )

    st.subheader("Cash Flow Statement")
    st.table(
        data=cash_flow_million.iloc[:, :5],
        border="horizontal"
    )
