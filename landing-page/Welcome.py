import dash
from dash import html, dcc

# Initialize the app
app = dash.Dash(__name__)
app.title = "UK Economic Growth Drivers Dashboard"

# Define the layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '40px'}, children=[
    html.H1("UK Economic Growth Drivers Dashboard", style={'textAlign': 'center', 'color': '#003366'}),
    
    html.H2("Purpose", style={'marginTop': '40px', 'color': '#004080'}),
    
    html.Div(
        id='purpose-container',
        children=[
            html.P(
                "This dashboard provides insights into the key drivers behind the UK's economic growth. "
                "It includes data visualizations and analysis of various economic indicators over time."
            ),
        ],
        style={
            'backgroundColor': '#f2f2f2',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
        }
    ),
    
    html.H2("Disclaimer", style={'marginTop': '40px', 'color': '#800000'}),
    
    html.Div(
        id='disclaimer-container',
        children=[
            html.P(
                "The information contained within this dashboard is for informational purposes only and "
                "should not be used as the basis for any financial or investment decisions."
            ),
        ],
        style={
            'backgroundColor': '#fff4f4',
            'padding': '20px',
            'borderRadius': '8px',
            'border': '1px solid #cc0000',
            'color': '#660000',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)'
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
