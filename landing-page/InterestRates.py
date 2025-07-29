from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

# Import your data loading functions
from IRDataLoad import get_latest_rates, get_full_timeseries

# Fetch data
df_latest = get_latest_rates()   # For circles (latest snapshot for key countries)
df_full = get_full_timeseries()  # For line chart (full timeseries for all countries)

# Prepare dropdown options from all countries in full dataset
all_countries = sorted(df_full['Country'].unique())

# Helper function to create a circular indicator for each country's interest rate
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

# Format the latest UK date for header display
uk_date = df_latest.loc[df_latest['Country'] == 'United Kingdom', 'Date'].max()
formatted_date = uk_date.strftime('%d %B %Y') if pd.notna(uk_date) else "N/A"

# Define your Dash page layout
interest_rates_layout = html.Div(style={'padding': '20px', 'fontFamily': 'Arial'}, children=[

    # Title and subtitle
    html.Div(style={'textAlign': 'left'}, children=[
        html.H1(
            "Let’s Explore Central Bank Interest Rates",
            style={'color': '#003366', 'fontSize': '20px', 'marginBottom': '5px'}
        ),
        # Sub heading title with dynamic date
        html.H3(f"Current Central Bank Interest Rates As At {formatted_date}", style={'color': '#666', 'marginTop': '0'})
    ]),

    # Main content: Circles left, line chart right
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'marginTop': '30px'}, children=[

        # Left column: Circles and commentary (fixed width)
        html.Div(style={'flex': '1', 'minWidth': '360px'}, children=[
            html.Div(style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'start'
            }, children=[
                rate_circle(row['Country'], row['Interest Rate'], row['Flag']) for _, row in df_latest.iterrows()
            ]),

            # Chart narrative below the interest rate circles
            html.Div(
                "The circles above represent the current interest rates as set by the Central Banks.",
                style={'marginTop': '20px', 'fontSize': '14px', 'color': '#333', 'textAlign': 'left'}
            ),
            # Text narrative explaining why Central Bank Interest Rates matter to the UK economy
            html.H3(
                "Why do Central Bank Interest Rates matter the UK economy?",
                style={'marginTop': '15px', 'color': '#003366', 'textAlign': 'left'}
            ),
            # Point 1 text
            html.Div(
                "📈 They influence borrowing costs – Higher interest rates make loans more expensive for households and businesses, which can slow down spending and investment.",
                style={'marginTop': '10px', 'fontSize': '14px', 'color': '#333', 'textAlign': 'left', 'maxWidth': '600px'}
            ),
            # Point 2 text
            html.Div(
                "💻 They affect inflation – Raising rates can help reduce inflation, while lowering rates can boost economic activity when inflation is low.",
                style={'marginTop': '10px', 'fontSize': '14px', 'color': '#333', 'textAlign': 'left', 'maxWidth': '600px'}
            ),
            # Point 3 text
            html.Div(
                "💷 They shape the strength of the pound – Higher rates can attract foreign investment, strengthening the currency, which influences imports and exports.",
                style={'marginTop': '10px', 'fontSize': '14px', 'color': '#333', 'textAlign': 'left', 'maxWidth': '600px'}
            )
        ]),

        # Right column: Create the line graph and filter for Central Bank interest rates over time
        html.Div(style={'flex': '2', 'paddingLeft': '40px'}, children=[
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in all_countries],
                value=all_countries,  # Select all countries
                multi=True,
                placeholder="Select countries to display"
            ),

            dcc.Graph(id='interest-rate-line-chart')
        ])
    ])
])

# Dash callback to update line chart based on dropdown selection
@callback(
    Output('interest-rate-line-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_line_chart(selected_countries):
    if not selected_countries:
        # If nothing selected, show empty chart
        return {}

    # Filter full timeseries by selected countries
    dff = df_full[df_full['Country'].isin(selected_countries)].copy()

    # Filter date starting from 2000-01-01
    #dff = dff[dff['Date'] >= pd.to_datetime('2005-01-01')]

    # Drop rows with missing values
    dff = dff.dropna(subset=['Date', 'Interest Rate'])

    # Sort by country and date
    dff = dff.sort_values(['Country', 'Date'])

    # Plot the line chart
    fig = px.line(
        dff,
        x='Date',
        y='Interest Rate',
        color='Country',
        title='Central Bank Policy Interest Rates Since 2005',
        labels={'Interest Rate': 'Interest Rate (%)'}
    )

    fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))
    return fig
