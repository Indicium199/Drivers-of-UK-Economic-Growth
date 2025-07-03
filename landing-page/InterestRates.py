from dash import html

def interest_rates_layout():
    return html.Div([
        html.H2("Interest Rates Analysis 📉"),
        html.P("This section will show visualizations and trends related to interest rates."),
        html.Div("📊 Placeholder for interest rate chart", style={
            'border': '1px dashed #999',
            'padding': '20px',
            'marginTop': '20px'
        })
    ])
