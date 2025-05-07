import dash
from dash import html, dcc, Input, Output

app = dash.Dash(__name__)
app.title = "UK Economic Growth Drivers Dashboard"

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '40px'}, children=[
    html.H1("📈 UK Economic Growth Drivers Dashboard 💰", style={'textAlign': 'center', 'color': '#003366'}),

    dcc.Tabs(id='tabs', value='welcome', children=[
        dcc.Tab(label='Welcome', value='welcome'),
        dcc.Tab(label='Interest Rates', value='interest-rates')
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
        return html.Div([
            html.H2("Interest Rates Analysis 📉"),
            html.P("This section will show visualizations and trends related to interest rates."),
            html.Div("📊 Placeholder for interest rate chart", style={
                'border': '1px dashed #999', 'padding': '20px', 'marginTop': '20px'
            })
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
