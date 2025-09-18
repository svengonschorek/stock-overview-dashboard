import yfinance as yf
import plotly.graph_objects as go

def load_waterfall(symbol):
    data = yf.Ticker(symbol)

    results_last_quarter = data.quarterly_financials[data.quarterly_financials.columns.values[0]]

    total_revenue = results_last_quarter.loc['Total Revenue']
    cogs = results_last_quarter.loc['Cost Of Revenue']
    gross_profit = results_last_quarter.loc['Gross Profit']
    op_expenses = results_last_quarter.loc['Operating Expense']
    op_income = results_last_quarter.loc['Operating Income']
    taxes_other = results_last_quarter.loc['Tax Provision']
    net_income = results_last_quarter.loc['Net Income']
    non_op_income = net_income - op_income + taxes_other

    y_values = [
        total_revenue,    # Revenue (absolute start)
        -cogs,            # COGS (deduction)
        gross_profit,     # Gross Profit (intermediate total, will be calculated by plotly from previous steps)
        -op_expenses,     # Op Expenses (deduction)
        op_income,        # Op Income (intermediate total)
        non_op_income,    # Non-Op Income/Expenses (addition)
        -taxes_other,     # Taxes & Other (deduction)
        net_income        # Net Income (absolute end)
    ]

    measures = [
        "absolute",   # Revenue
        "relative",   # COGS (deduction from Revenue)
        "total",      # Gross Profit (Revenue - COGS)
        "relative",   # Op Expenses (deduction from Gross Profit)
        "total",      # Op Income (Gross Profit - Op Expenses)
        "relative",   # Non-Op income/expenses (addition/subtraction)
        "relative",   # Taxes & Other (deduction)
        "absolute"    # Net Income (final absolute value)
    ]

    labels = [
        "Revenue",
        "COGS",
        "Gross Profit",
        "Op Expenses",
        "Op Income",
        "Non-Op income/expenses",
        "Taxes & Other",
        "Net Income"
    ]

    deltas = [
        0,
        -cogs,
        0,
        -op_expenses,
        0,
        non_op_income,
        -taxes_other,
        0
    ] 

    fig = go.Figure(
        go.Waterfall(
            name="Financial Overview",
            orientation="v",
            measure=measures,
            x=labels,
            y=y_values,
            customdata=deltas,
            hoverinfo="y+name",
            hovertemplate=(
                f"%{{y:,.0f}} {data.info['financialCurrency']}<br>"
                f"Delta: %{{customdata:,.0f}} {data.info['financialCurrency']}<extra></extra>"
            ),
            increasing={"marker":{"color": "#5ab18f"}},
            decreasing={"marker":{"color": "#ea5e77"}},
            totals={"marker":{"color": "#4285f4"}},
            connector={"mode":"between", "line":{"width":1, "color":"rgb(0, 0, 0)", "dash":"dot"}}
        )
    )

    fig.update_yaxes(
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="gray"
    )

    fig.update_layout(
        title_text=f"Revenue to Net Income Conversion [in {data.info['financialCurrency']}]",
        showlegend=False,
        xaxis_title="",
        yaxis_title="Amount (B)",
        margin=dict(l=50, r=50, t=80, b=50),
        template="plotly_white", # Clean white background
    )
    

    #st.plotly_chart(fig, use_container_width=True)
    return fig
