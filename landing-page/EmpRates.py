from dash import html
import pandas as pd
from EmpRatesLoad import get_latest_unemployment

# Load the full unemployment timeseries
df_latest = get_latest_unemployment()

# Get the latest row (last date)
latest_row = df_latest.sort_values('Date').iloc[-1]

# Extract values
rate = latest_row['Unemployment Rate']
date = latest_row['Date']
country = latest_row['Country']

# Create KPI circle
def unemployment_kpi_circle(country, rate, date):
    formatted_date = date.strftime('%d %b %Y') if pd.notna(date) else "N/A"
    return html.Div(style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'flex-start',
    }, children=[
        html.Div(style={
            'width': '140px',
            'height': '140px',
            'borderRadius': '50%',  # perfect circle
            'backgroundColor': '#003366',
            'color': 'white',
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'fontWeight': 'bold',
            'fontSize': '24px',
            'boxShadow': '0 4px 10px rgba(0,0,0,0.2)',
            'marginBottom': '10px'
        }, children=[
            html.Div(f"{rate:.1f}%", style={'fontSize': '36px'})
        ]),
        html.Div(country, style={'fontSize': '18px', 'color': '#003366', 'marginBottom': '5px'}),
        html.Div(f"as of {formatted_date}", style={'fontSize': '12px', 'color': '#666'})
    ])

# Layout
unemployment_kpi_component = html.Div(style={
    'padding': '20px',
    'fontFamily': 'Arial'
}, children=[
    html.H1("Lets explore UK Wages & Employment rates", style={
        'color': '#003366',
        'fontSize': '24px',
        'textAlign': 'left'
    }),

    html.H3(f"Seasonally Adjusted Unemployment Rate {date.strftime('%d %B %Y')}", style={
        'color': '#666',
        'textAlign': 'left',
        'marginTop': '0'
    }),

    # KPI block (circle + text below it)
    unemployment_kpi_circle(country, rate, date),

    # Explanatory paragraph under everything
    html.Div(
        "This is the current seasonally adjusted unemployment rate for those aged 16 and over in the United Kingdom",
        style={
            'marginTop': '20px',
            'fontSize': '14px',
            'color': '#333',
            'maxWidth': '600px',
            'textAlign': 'left'
        }
    )
])
