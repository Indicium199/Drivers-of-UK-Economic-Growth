from dash import html
import pandas as pd

# Assume you've already created and cleaned the interest rate dataframe in IRDataLoad.py
from IRDataLoad import get_latest_rates  # You should define and import this function

# Fetch data (expects a DataFrame with Country, Rate, Flag columns)
df = get_latest_rates()

# Helper to create a circle indicator
def rate_circle(country, rate, flag):
    return html.Div(style={
        'width': '120px',
        'height': '120px',
        'borderRadius': '60px',
        'backgroundColor': '#003366',
        'color': 'white',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'margin': '10px',
        'fontWeight': 'bold',
        'fontSize': '20px',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.2)'
    }, children=[
        html.Div(f"{rate:.2f}%", style={'fontSize': '24px'}),
        html.Div(style={'marginTop': '5px', 'fontSize': '16px'}, children=[
            html.Div(f"{flag}", style={'fontSize': '22px'}),
            html.Div(country, style={'fontSize': '12px'})
        ])
    ])

# Build the layout
interest_rates_layout = html.Div(style={'padding': '40px', 'fontFamily': 'Arial'}, children=[
    html.Div(style={'textAlign': 'left'}, children=[
        html.H1("Let’s Explore Central Bank Interest Rates", style={'color': '#003366'}),
        html.H3("Current Central Bank interest rates", style={'color': '#666', 'marginTop': '0'})
    ]),
    
    html.Div(style={
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'start',
        'marginTop': '30px',
        'flexWrap': 'wrap'
    }, children=[
        rate_circle(row['Country'], row['Interest Rate'], row['Flag']) for _, row in df.iterrows()
    ])
])
