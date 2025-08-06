# Import Dash framework
import dash
# Import required Dash components
from dash import html, dcc, Input, Output
# Import the layout for interest rates and GDP
from InterestRates import interest_rates_layout
from GDP import layout as gdp_layout, register_callbacks  # import callback registrar for GDP

# Initialise the Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True)
# Create the title of the dashboard
app.title = "UK Economic Growth Drivers Dashboard"

# Register callbacks from GDP module (and others if needed)
register_callbacks(app)

# Define the layout of the dashboard
app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',  # Set the global font style
        'padding': '40px'  # Add padding around the page content
    },
    children=[
        # Main page title
        html.H1(
            "📈 UK Economic Growth Drivers Dashboard 💰",  # Title of dashboard
            style={
                'textAlign': 'center',  # Align text center
                'color': '#003366'  # Text colour
            }
        ),
        # Create set of tabs for navigating the dashboard
        dcc.Tabs(
            id='tabs',  # ID for the tabs
            value='welcome',  # Default tab
            children=[
                dcc.Tab(label='Welcome', value='welcome'),
                dcc.Tab(label='Interest Rates', value='interest-rates'),
                dcc.Tab(label='Employment & Wages', value='employment-wages'),
                dcc.Tab(label='Cost of Living', value='cost-of-living'),
                dcc.Tab(label='Gross Domestic Product', value='gdp'),
            ]
        ),
        # Placeholder for content based on selected tab
        html.Div(
            id='tab-content',
            style={'marginTop': '30px'}  # Add spacing above the content
        )
    ]
)

# Callback to update the tab content dynamically
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    # Content for the Welcome tab
    if tab == 'welcome':
        return html.Div([
            # Main content: two columns
            html.Div(
                style={'display': 'flex', 'justifyContent': 'space-between'},
                children=[
                    # Left column
                    html.Div(
                        style={'width': '48%', 'paddingRight': '20px'},
                        children=[
                            html.H2("Dashboard Purpose", style={'color': '#003366'}),
                            html.P(
                                "This dashboard provides a simplified consolidated view of key economic indicators "
                                "that influence the UK's economic growth. It contains data on:"
                            ),
                            html.Ul([
                                html.Li("📊 Interest Rate Data – UK & Global"),
                                html.Li("🌍 Gross Domestic Product (GDP) – UK & Global"),
                                html.Li("💼 Wages Data – UK only"),
                                html.Li("🛒 Cost of Living Data – UK only"),
                            ]),
                            html.H3("Commentary Preference", style={'color': '#003366'}),
                            dcc.RadioItems(
                                id='commentary-type',
                                options=[
                                    {'label': 'Simple', 'value': 'simple'},
                                    {'label': 'Complex', 'value': 'complex'}
                                ],
                                value='simple',
                                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
                            )
                        ]
                    ),
                    # Right column
                    html.Div(
                        style={'width': '48%'},
                        children=[
                            html.H2("How to Use the Dashboard", style={'color': '#003366'}),
                            html.P([
                                html.Em([
                                    html.Strong("Get started by clicking on the tabs above to explore the data!")
                                ])
                            ]),
                            html.P("Each tab contains useful charts and short explainers to help you understand what drives UK economic growth."),
                            html.H3("Hints and Tips", style={'color': '#003366'}),
                            html.Ul([
                                html.Li("Hover over charts for more detail."),
                                html.Li("Use filters to refine what data is displayed."),
                                html.Li("Check data sources at the bottom of each section.")
                            ])
                        ]
                    )
                ]
            ),
            # Bottom warning box
            html.Div(
                style={
                    'marginTop': '40px',
                    'padding': '20px',
                    'backgroundColor': '#fff3cd',
                    'color': '#856404',
                    'border': '1px solid #ffeeba',
                    'borderRadius': '5px',
                    'fontWeight': 'bold',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center'
                },
                children=[
                    html.Span("⚠️", style={'fontSize': '24px', 'marginRight': '10px'}),
                    html.Span("The information presented in this dashboard is for informational and educational purposes only. "
                              "It should not be interpreted as financial advice or used for investment decisions. "
                              "Always consult a qualified financial advisor before making financial choices.")
                ]
            )
        ])

    # Content for the Interest Rates tab
    elif tab == 'interest-rates':
        return interest_rates_layout  # Imported from InterestRates.py

    # Content for Employment & Wages tab
    elif tab == 'employment-wages':
        return html.Div([
            html.H2("Employment & Wages"),
            html.P("Content for Employment & Wages tab goes here.")
        ])

    # Content for Cost of Living tab
    elif tab == 'cost-of-living':
        return html.Div([
            html.H2("Cost of Living"),
            html.P("Content for Cost of Living tab goes here.")
        ])

    # Content for Gross Domestic Product tab
    elif tab == 'gdp':
        return gdp_layout

# Start the Dash app server
if __name__ == '__main__':
    app.run_server(debug=True)
