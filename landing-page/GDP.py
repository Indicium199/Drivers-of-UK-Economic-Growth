from dash import html, dash_table
from dash.dash_table.Format import Format, Scheme
from GDPDataLoader import get_g10_gdp_change

# Load and prepare the data
df_gdp = get_g10_gdp_change(2023, 2024).reset_index()

# Select relevant columns
df_display = df_gdp[['Country', 'GDP Change (Trillions)', '% Change']].copy()

# Map of G10 countries to flag emojis
flag_map = {
    'United States': '🇺🇸',
    'United Kingdom': '🇬🇧',
    'Germany': '🇩🇪',
    'France': '🇫🇷',
    'Italy': '🇮🇹',
    'Canada': '🇨🇦',
    'Japan': '🇯🇵',
    'Netherlands': '🇳🇱',
    'Sweden': '🇸🇪',
    'Switzerland': '🇨🇭',
    'Belgium': '🇧🇪'
}

# Add flag emoji to Country name
df_display['Country'] = df_display['Country'].apply(lambda x: f"{flag_map.get(x, '')} {x}")

# Round % Change for neat display
df_display['% Change'] = df_display['% Change'].round(2)

# Add arrows (up/down) with color-coded text for % Change
def format_percent_change(val):
    if val > 0:
        return f"↑ {val}%"
    elif val < 0:
        return f"↓ {val}%"
    else:
        return f"{val}%"

df_display['% Change'] = df_display['% Change'].apply(format_percent_change)

# Create Dash DataTable
data_table = dash_table.DataTable(
    columns=[
        {"name": "Country", "id": "Country"},
        {"name": "GDP Change (Trillions)", "id": "GDP Change (Trillions)", 'type': 'numeric', 'format': Format(precision=2, scheme=Scheme.fixed)},
        {"name": "% Change", "id": "% Change", "type": "text"},
    ],
    data=df_display.to_dict('records'),
    style_table={'overflowX': 'auto', 'maxWidth': '700px'},
    style_cell={
        'fontSize': '12px',
        'padding': '6px 8px',
        'minWidth': '80px', 'width': '120px', 'maxWidth': '150px',
        'whiteSpace': 'normal',
        'textAlign': 'left',
    },
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold',
        'fontSize': '13px',
        'textAlign': 'left'
    },
    style_data_conditional=[
        {
            'if': {
                'filter_query': '{% Change} contains "↑"',
                'column_id': '% Change'
            },
            'color': 'green',
            'fontWeight': 'bold',
        },
        {
            'if': {
                'filter_query': '{% Change} contains "↓"',
                'column_id': '% Change'
            },
            'color': 'red',
            'fontWeight': 'bold',
        },
    ],
    page_size=10,
)

# Layout for the GDP tab
layout = html.Div([
    html.H1("Let's Explore Gross Domestic Product (GDP)", style={'color': '#003366', 'fontSize': '20px'}),
    html.H3("G10 Countries Ranked % GDP Change", style={'color': '#666', 'marginTop': '0'}),
    html.Div([
        # Left column: table
        html.Div(data_table, style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        # Right column: placeholder for visualizations
        html.Div([
            html.P("Visualisations go here")
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '20px'})
    ])
])
