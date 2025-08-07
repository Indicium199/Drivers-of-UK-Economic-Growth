from dash import html, dash_table, dcc, Input, Output
from dash.dash_table.Format import Format, Scheme
import plotly.express as px
from GDPDataLoader import get_g10_gdp_change, get_g10_gdp_timeseries  # load in the functions for the underlying table/chart dataframes

# Load data for table (GDP change 2023-2024)
df_gdp_change = get_g10_gdp_change(2023, 2024).reset_index()

# Load time series data for line chart (2000-2024)
df_timeseries = get_g10_gdp_timeseries(2000, 2024)

# Prepare data for display table
df_display = df_gdp_change[['Country', 'GDP Change (Trillions)', '% Change']].copy()
# Map flag emojis to countries
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

df_display['Country'] = df_display['Country'].apply(lambda x: f"{flag_map.get(x, '')} {x}")
df_display['% Change'] = df_display['% Change'].round(2)

def format_percent_change(val):
    if val > 0:
        return f"↑ {val}%"
    elif val < 0:
        return f"↓ {val}%"
    else:
        return f"{val}%"

df_display['% Change'] = df_display['% Change'].apply(format_percent_change)

data_table = dash_table.DataTable(
    columns=[
        {"name": "Country", "id": "Country"},
        {"name": "GDP Change (Trillions)", "id": "GDP Change (Trillions)", 'type': 'numeric', 'format': Format(precision=2, scheme=Scheme.fixed)},
        {"name": "% Change", "id": "% Change", "type": "text"},
    ],
    data=df_display.to_dict('records'),
    style_table={'overflowX': 'auto', 'maxWidth': '700px'},
    style_cell={
        'fontSize': '10px',
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

# Dropdown options for filtering countries (without flags)
dropdown_options = [{"label": c, "value": c} for c in sorted(df_timeseries["Country"].unique())]

layout = html.Div([
    html.H1("Let's Explore Gross Domestic Product (GDP)", style={'color': '#003366', 'fontSize': '20px'}),
    html.H3("G10 Countries % GDP Change", style={'color': '#666', 'marginTop': '0'}),
    
    html.Div([
        # Left side: DataTable and narrative
        html.Div([
            data_table,
            html.P(
                "The table above shows the % change in GDP from 2023 to 2024 for the G10 nations.",
                style={'fontSize': '14px', 'color': '#555', 'marginTop': '10px'}
            ),
            html.H3(
                "Why does GDP matter to the UK economy?",
                style={'color': '#666', 'marginTop': '20px'}
            ),
            html.P("🌱 GDP is a good indicator of whether the UK economy is growing or shrinking.",
                   style={'fontSize': '14px', 'color': '#555', 'marginTop': '5px'}),
            html.P("💻 A stronger GDP usually means better business conditions and more jobs.",
                   style={'fontSize': '14px', 'color': '#555', 'marginTop': '5px'}),
            html.P("🚌 The government uses GDP to decide how much to spend on public services like schools, healthcare and transport.",
                   style={'fontSize': '14px', 'color': '#555', 'marginTop': '5px'})
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Right side: Country filter and line graph
        html.Div([
            dcc.Dropdown(
                id='country-filter',
                options=dropdown_options,
                multi=True,
                value=[option['value'] for option in dropdown_options],  # default select all
                placeholder="Select countries to display"
            ),
            dcc.Graph(id='gdp-line-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '20px'})
    ])
])

def register_callbacks(app):
    @app.callback(
        Output('gdp-line-chart', 'figure'),
        Input('country-filter', 'value')
    )
    def update_gdp_line_chart(selected_countries):
        if not selected_countries:
            return {}
        filtered_df = df_timeseries[df_timeseries['Country'].isin(selected_countries)]
        fig = px.line(
            filtered_df,
            x='Year',
            y='GDP (Trillions US$)',
            color='Country',
            markers=True,
            title="GDP Over Time (Trillions US$)"
        )
        fig.update_layout(legend_title_text='Country')
        return fig
