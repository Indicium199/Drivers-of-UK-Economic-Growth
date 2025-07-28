# Import libraries
from dash import html  # Import HTML from Dash
import pandas as pd   # Import pandas for data manipulation

# Import the get_latest_rates function to get latest interest rate data for selected countries
from IRDataLoad import get_latest_rates 

# Fetch the latest interest rate data as a dataframe
df = get_latest_rates()

# Helper function to create a circular indicator for each country's interest rate
def rate_circle(country, rate, flag):
    return html.Div(style={
        'width': '120px',              # Fixed width for the circle
        'height': '120px',             # Fixed height for the circle
        'borderRadius': '60px',        # Rounded corners to make the circle (half width)
        'backgroundColor': '#003366',  # Dark blue background
        'color': 'white',              # White text
        'display': 'flex',             # Flexbox layout
        'flexDirection': 'column',     # Stack children vertically
        'alignItems': 'center',        # Center horizontally
        'justifyContent': 'center',    # Center vertically
        'margin': '10px',              # Margin around circle
        'fontWeight': 'bold',          # Bold text
        'fontSize': '20px',            # Font size
        'boxShadow': '0 4px 10px rgba(0,0,0,0.2)'  # Shadow effect
    }, children=[
        html.Div(f"{rate:.2f}%", style={'fontSize': '24px'}),  # Interest rate text
        html.Div(style={'marginTop': '5px', 'fontSize': '16px'}, children=[
            html.Div(f"{flag}", style={'fontSize': '22px'}),    # Country flag emoji
            html.Div(country, style={'fontSize': '12px'})       # Country name
        ])
    ])

# Extract latest UK date in a readable format, e.g. '2025-07-28'
uk_date = df.loc[df['Country'] == 'United Kingdom', 'Date'].max()

# Format the date as a string, e.g. '28 July 2025'
if pd.notna(uk_date):
    formatted_date = uk_date.strftime('%d %B %Y')
else:
    formatted_date = "N/A"  # fallback if date missing

# Build the layout container for the Dash app
interest_rates_layout = html.Div(style={'padding': '20px', 'fontFamily': 'Arial'}, children=[
    html.Div(style={'textAlign': 'left'}, children=[
        # Title
        html.H1(
            "Let’s Explore Central Bank Interest Rates",
            style={'color': '#003366', 'fontSize': '20px', 'marginBottom': '5px'}
        ),
        #html.H3("Current Central Bank Interest Rates", style={'color': '#666', 'marginTop': '0'})
        html.H3(f"Current Central Bank Interest Rates As At {formatted_date}", style={'color': '#666', 'marginTop': '0'})
    ]),

    # Container for the interest rate circles
    html.Div(style={
        'display': 'flex',          # Flexbox row
        'flexDirection': 'row',     # Horizontal layout
        'justifyContent': 'start',  # Align left
        'marginTop': '30px',        # Margin top
        'flexWrap': 'wrap'          # Wrap on multiple lines
    }, children=[
        rate_circle(row['Country'], row['Interest Rate'], row['Flag']) for _, row in df.iterrows()
    ]),

    # Commentary text box under the circles
    html.Div(
        "The circles above represent the current interest rates as set by the Central Banks.",
        style={
            'marginTop': '20px',   # Space above text
            'fontSize': '14px',    # Text size
            'color': '#333',       # Text color
            'textAlign': 'left'    # Align left
        }
    ),

    # Subtitle below the commentary text
    html.H3(
        "Why do Central Bank Interest Rates matter the UK economy?",
        style={
            'marginTop': '15px',   # Space above subtitle
            'color': '#003366',    # Dark blue color
            'textAlign': 'left'    # Align left
        }
    ),
    html.Div(
        "📈 They influence borrowing costs – Higher interest rates make loans more expensive for households and businesses, which can slow down spending and investment.",
        style={
            'marginTop': '10px',
            'fontSize': '14px',
            'color': '#333',
            'textAlign': 'left',
             'maxWidth': '600px'
        }
    ),
    # Second text block with laptop emoji
    html.Div(
        "💻 They affect inflation – Raising rates can help reduce inflation, while lowering rates can boost economic activity when inflation is low.",
        style={
            'marginTop': '10px',
            'fontSize': '14px',
            'color': '#333',
            'textAlign': 'left',
            'maxWidth': '600px'
        }
    ),
    # Third text block with twenty pound note emoji
    html.Div(
        "💷 They shape the strength of the pound – Higher rates can attract foreign investment, strengthening the currency, which influences imports and exports.",
        style={
            'marginTop': '10px',
            'fontSize': '14px',
            'color': '#333',
            'textAlign': 'left',
            'maxWidth': '600px'
        }
    )
])
