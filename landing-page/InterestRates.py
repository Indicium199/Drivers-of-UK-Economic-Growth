from dash import html

def interest_rates_layout():
    return html.Div([
        html.H2("Interest Rates Analysis 📉"),
        html.P("This section will show visualizations and trends related to interest rates."),

        # 🔹 Graphic row: Left = rate, Right = info box
        html.Div([
            # Left box: UK interest rate
            html.Div([
                html.H3("🇬🇧 UK Bank of England Current Interest Rate"),
                html.Div("4.5%", style={
                    'fontSize': '40px',
                    'fontWeight': 'bold',
                    'color': '#003366',
                    'padding': '20px',
                    'backgroundColor': '#e6f0ff',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'boxShadow': '0 2px 6px rgba(0,0,0,0.1)'
                })
            ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            # Right box: info / prompt
            html.Div([
                html.Div("💬 Tell me about central bank interest rates", style={
                    'fontSize': '18px',
                    'padding': '20px',
                    'backgroundColor': '#f2f2f2',
                    'borderRadius': '10px',
                    'height': '100%',
                    'boxShadow': '0 2px 6px rgba(0,0,0,0.05)'
                })
            ], style={'width': '50%', 'display': 'inline-block', 'marginLeft': '5%'})
        ], style={'marginTop': '30px'}),

        # Placeholder chart section
        html.Div("📊 Placeholder for interest rate chart", style={
            'border': '1px dashed #999',
            'padding': '20px',
            'marginTop': '30px'
        })
    ])

