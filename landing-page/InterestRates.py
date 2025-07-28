# Import libraries
from dash import html # Import HTML from Dash
import pandas as pd # Import pandas for data manipulation

# Import the get_latest_rates function to get latest interest rate data for selected countries
from IRDataLoad import get_latest_rates 

# Fetch the latest interest rate data as a dataframe
df = get_latest_rates()

# Helper function to create a circular indicator for each countries interest rate
def rate_circle(country, rate, flag):
    return html.Div(style={
        'width': '120px', # Fixed width for the circle
        'height': '120px', # Fixed height for the circle
        'borderRadius': '60px', # Rounded corners to make the circle - half of width vs height
        'backgroundColor': '#003366', # Dark blue background in the circle
        'color': 'white', # White text
        'display': 'flex', # Flexbox for layout
        'flexDirection': 'column', #Stack the children vertically
        'alignItems': 'center', # Centre the children horizontally
        'justifyContent': 'center', # Centre the children vertically
        'margin': '10px', # Create a margin around each circle
        'fontWeight': 'bold', # Make the text bold
        'fontSize': '20px', # Font size
        'boxShadow': '0 4px 10px rgba(0,0,0,0.2)' # Use a shadow
    }, children=[
        # Format interest rate to 2 d.p with a percentage sign
        html.Div(f"{rate:.2f}%", style={'fontSize': '24px'}),
        # Create a container for the flag and country name with a margin
        html.Div(style={'marginTop': '5px', 'fontSize': '16px'}, children=[
            html.Div(f"{flag}", style={'fontSize': '22px'}), # Display the country flag emoji
            html.Div(country, style={'fontSize': '12px'}) # Display the country name
        ])
    ])

# Build the layout container for the Dash app
interest_rates_layout = html.Div(style={'padding': '20px', 'fontFamily': 'Arial'}, children=[
    html.Div(style={'textAlign': 'left'}, children=[
        # Title of the text box
        html.H1(
    "Let’s Explore Central Bank Interest Rates",
    style={'color': '#003366', 'fontSize': '20px', 'marginBottom': '5px'}
),

        html.H3("Current Central Bank Interest Rates", style={'color': '#666', 'marginTop': '0'})
    ]),
    # Container for the interest rate circles
    html.Div(style={
        'display': 'flex', #Flex box to arrange the children in a row
        'flexDirection': 'row', # Horizontal layout
        'justifyContent': 'start', # Align circles to the left
        'marginTop': '30px', # Margin around the container
        'flexWrap': 'wrap' # Allow the circles to wrap on multiple lines
    # Create a circle for each country in the data frame    
    }, children=[
        rate_circle(row['Country'], row['Interest Rate'], row['Flag']) for _, row in df.iterrows()
    ])
])


