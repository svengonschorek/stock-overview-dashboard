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
        # Filter stocks by sector
        sector_stocks = stocks_df[stocks_df['sector'] == sector]

        if not sector_stocks.empty:
            # Display sector header
            st.header(sector)
            df = sector_stocks[['rank', 'name', 'symbol', 'country', 'industry']].reset_index(drop=True).rename(columns={
                'rank': 'Rank',
                'name': 'Name',
                'symbol': 'Symbol',
                'country': 'Country',
                'industry': 'Industry',
            })

            # Create a column with the link URL
            df['Symbol Link'] = df['Symbol'].apply(lambda x: f"?symbol={x}")

            # Display the data editor with clickable links
            st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Symbol Link": st.column_config.LinkColumn(
                        label="",
                        display_text="→",
                        width=10,
                    ),
                },
                disabled=["Symbol Link"],
            )
