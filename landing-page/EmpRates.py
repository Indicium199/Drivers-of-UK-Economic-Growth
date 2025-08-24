from dash import html, dcc
import pandas as pd
import plotly.express as px
from EmpRatesLoad import get_latest_unemployment, get_latest_awe  

# -------------------------------
# Load data
# -------------------------------
df_latest = get_latest_unemployment()
df_awe = get_latest_awe()

latest_row = df_latest.sort_values('Date').iloc[-1]
rate = latest_row['Unemployment Rate']
date = latest_row['Date']
country = latest_row['Country']

# -------------------------------
# KPI circle component
# -------------------------------
def unemployment_kpi_circle(country, rate, date):
    formatted_date = date.strftime('%d %b %Y') if pd.notna(date) else "N/A"
    return html.Div(style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'marginTop': '10px'
    }, children=[
        html.Div(style={
            'width': '140px',
            'height': '140px',
            'borderRadius': '50%',
            'backgroundColor': '#003366',
            'color': 'white',
            'display': 'flex',
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

# -------------------------------
# Line graph for AWE
# -------------------------------
fig_awe = px.line(df_awe, x='Date', y='Average Weekly Earnings')
fig_awe.update_layout(
    margin=dict(l=0, r=0, t=30, b=0),
    height=350,
    xaxis_title='',
    yaxis_title='Earnings (£)',
    font=dict(size=12)
)

line_graph_component = dcc.Graph(
    figure=fig_awe,
    style={'width': '100%', 'height': '350px'}
)

# -------------------------------
# Header row: left and right titles
# -------------------------------
header_row = html.Div(style={
    'display': 'flex',
    'flexDirection': 'row',
    'justifyContent': 'space-between',
    'alignItems': 'flex-start',
    'width': '100%'
}, children=[
    # Left title
    html.H3(f"Seasonally Adjusted Unemployment Rate {date.strftime('%d %B %Y')}", style={
        'color': '#666',
        'textAlign': 'left',
        'margin': '0'
    }),
    
    # Right title
    html.H3("Average Weekly Earnings Over Time", style={
        'color': '#003366',
        'textAlign': 'right',
        'margin': '0'
    })
])

# -------------------------------
# Content row: left KPI, right graph
# -------------------------------
content_row = html.Div(style={
    'display': 'flex',
    'flexDirection': 'row',
    'justifyContent': 'space-between',
    'alignItems': 'flex-start',
    'marginTop': '10px',
    'width': '100%'
}, children=[
    # LEFT COLUMN: KPI circle + explanatory text
    html.Div(style={'flex': '0 0 300px'}, children=[
        unemployment_kpi_circle(country, rate, date),
        html.Div(
            "This is the current seasonally adjusted unemployment rate for those aged 16 and over in the United Kingdom",
            style={
                'marginTop': '20px',
                'fontSize': '14px',
                'color': '#333',
                'textAlign': 'left',
                'maxWidth': '300px'
            }
        )
    ]),

    # RIGHT COLUMN: line graph aligned with right-hand title
    html.Div(style={'flex': '0 0 600px', 'textAlign': 'left'}, children=[
        line_graph_component
    ])
])

# -------------------------------
# Full layout
# -------------------------------
unemployment_kpi_component = html.Div(style={
    'padding': '20px',
    'fontFamily': 'Arial',
    'width': '100%'
}, children=[
    html.H1("Let's explore UK Wages & Employment rates", style={
        'color': '#003366',
        'fontSize': '24px',
        'textAlign': 'left',
        'marginBottom': '10px'
    }),
    header_row,
    content_row
])
