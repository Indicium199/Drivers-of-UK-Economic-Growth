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
        dcc.Tab(label='Placeholder 1', value='placeholder-1'),
        dcc.Tab(label='Placeholder 2', value='placeholder-2'),
        dcc.Tab(label='Placeholder 3', value='placeholder-3'),
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
            html.H2("Purpose"),
            html.Div(id='purpose-container', children=[
                html.P("This dashboard provides insights into the key drivers behind the UK's economic growth.")
            ]),
            html.H2("Please select whether you would prefer simple or complex commentary"),
            dcc.RadioItems(
                id='commentary-type',
                options=[
                    {'label': 'Simple', 'value': 'simple'},
                    {'label': 'Complex', 'value': 'complex'}
                ],
                value='simple',
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            ),
            html.H2("Disclaimer"),
            html.Div(id='disclaimer-container', children=[
                html.P("The information in this dashboard should not be used for financial decisions.")
            ])
        ])
    elif tab == 'interest-rates':
        return interest_rates_layout()

    elif tab == 'placeholder-1':
        return html.Div([
            html.H2("Placeholder 1"),
            html.P("Content for Placeholder 1 tab goes here.")
        ])
    elif tab == 'placeholder-2':
        return html.Div([
            html.H2("Placeholder 2"),
            html.P("Content for Placeholder 2 tab goes here.")
        ])
    elif tab == 'placeholder-3':
        return html.Div([
            html.H2("Placeholder 3"),
            html.P("Content for Placeholder 3 tab goes here.")
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
