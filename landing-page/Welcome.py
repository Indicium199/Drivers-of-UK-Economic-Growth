import dash
from dash import html, dcc, Input, Output
from InterestRates import interest_rates_layout

app = dash.Dash(__name__)
app.title = "UK Economic Growth Drivers Dashboard"

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '40px'}, children=[
    html.H1("📈 UK Economic Growth Drivers Dashboard 💰", style={'textAlign': 'center', 'color': '#003366'}),

    dcc.Tabs(id='tabs', value='welcome', children=[
        dcc.Tab(label='Welcome', value='welcome'),
        dcc.Tab(label='Interest Rates', value='interest-rates'),
        dcc.Tab(label='Employment & Wages', value='employment-wages'),
        dcc.Tab(label='Cost of Living', value='cost-of-living'),
        dcc.Tab(label='Gross Domestic Product', value='gdp'),
    ]),

    html.Div(id='tab-content', style={'marginTop': '30px'})
])

@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'welcome':
        return html.Div([
            # Top 2-column layout
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between'}, children=[

                # Left: Dashboard Purpose
                html.Div(style={'width': '48%', 'paddingRight': '20px'}, children=[
                    html.H2("Dashboard Purpose"),
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
                    html.H3("Commentary Preference"),
                    dcc.RadioItems(
                        id='commentary-type',
                        options=[
                            {'label': 'Simple', 'value': 'simple'},
                            {'label': 'Complex', 'value': 'complex'}
                        ],
                        value='simple',
                        labelStyle={'display': 'inline-block', 'marginRight': '20px'}
                    )
                ]),

                # Right: How to Use & Hints and Tips
                html.Div(style={'width': '48%'}, children=[
                    html.H2("How to Use the Dashboard"),
                    html.P([
                        html.Em([
                            html.Strong("Get started by clicking on the tabs above to explore the data!")
                        ])
                    ]),
                    html.P("Each tab contains useful charts and short explainers to help you understand what drives UK economic growth."),

                    html.H3("Hints and Tips"),
                    html.Ul([
                        html.Li("Hover over charts for more detail."),
                        html.Li("Use filters to refine what data is displayed."),
                        html.Li("Check data sources at the bottom of each section.")
                    ])
                ])
            ]),

            # Bottom full-width warning box
            html.Div(style={
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
            }, children=[
                html.Span("⚠️", style={'fontSize': '24px', 'marginRight': '10px'}),
                html.Span("The information presented in this dashboard is for informational and educational purposes only. "
                          "It should not be interpreted as financial advice or used for investment decisions. "
                          "Always consult a qualified financial advisor before making financial choices.")
            ])
        ])
    
    elif tab == 'interest-rates':
        return interest_rates_layout()

    elif tab == 'employment-wages':
        return html.Div([
            html.H2("Employment & Wages"),
            html.P("Content for Employment & Wages tab goes here.")
        ])
    
    elif tab == 'cost-of-living':
        return html.Div([
            html.H2("Cost of Living"),
            html.P("Content for Cost of Living tab goes here.")
        ])

    elif tab == 'gdp':
        return html.Div([
            html.H2("Gross Domestic Product"),
            html.P("Content for GDP tab goes here.")
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
