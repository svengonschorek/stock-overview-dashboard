import streamlit as st
import pandas as pd

def get_stocks_data():
    path = 'data/stocks.csv'
    df = pd.read_csv(path)
    return df

def stocks_list():
    st.title("All Stocks by Sector")
    st.subheader("A comprehensive list of stocks categorized by sector.")

    stocks_df = get_stocks_data()

    sectors = stocks_df['sector'].unique()
    for sector in sectors:
        sector_stocks = stocks_df[stocks_df['sector'] == sector]
        if not sector_stocks.empty:
            st.header(sector)
            st.dataframe(
                sector_stocks[['rank', 'name', 'symbol', 'country', 'industry']].reset_index(drop=True).rename(columns={
                    'rank': 'Rank',
                    'name': 'Name',
                    'symbol': 'Symbol',
                    'country': 'Country',
                    'industry': 'Industry',
                }),
                width='stretch',
                hide_index=True,
                )
