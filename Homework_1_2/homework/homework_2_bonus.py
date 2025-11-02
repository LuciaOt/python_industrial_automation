import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os
from pathlib import Path

'''
Script Fetches Czech wage data and creates an interactive web app with filters
'''

class CZSODashApp:
    
    def __init__(self, dataset_id='110080'):
        self.dataset_id = dataset_id
        self.df = None
        self.app = None
        self.csv_filepath = None
        
    def fetch_data(self):
        print(f"Fetching data for dataset {self.dataset_id}...")
        url = "https://vdb.czso.cz/pll/eweb/package_show"
        response = requests.get(url, params={'id': self.dataset_id})
        
        if response.status_code != 200:
            print("Failed to fetch metadata")
            return False
        
        metadata = response.json()
        result = metadata.get('result', {})
       
        resources = result.get('resources', [])
        csv_url = None
        
        for resource in resources:
            if 'csv' in resource.get('format', '').lower():
                csv_url = resource.get('url')
                break
        
        if not csv_url:
            print("No CSV found")
            return False
        
        print(f"Downloading from: {csv_url}")
        
        script_dir = Path(__file__).parent.resolve()
        self.csv_filepath = script_dir / f"czso_data_{self.dataset_id}.csv"
        
        try:
            self.df = pd.read_csv(csv_url, encoding='utf-8')
        except:
            self.df = pd.read_csv(csv_url, encoding='windows-1250')
        
        try:
            self.df.to_csv(self.csv_filepath, index=False, encoding='utf-8')
            print(f"✓ Data saved to: {self.csv_filepath}")
        except Exception as e:
            print(f"⚠ Warning: Could not save CSV file: {e}")
        
        print(f"Data loaded! Shape: {self.df.shape}")
        
        # Convert numeric columns to native Python types for Plotly compatibility
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            if self.df[col].dtype == 'int64':
                self.df[col] = self.df[col].astype('Int64')
        
        return True
    
    def create_app(self):
       
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        
        regions = sorted([str(r) for r in self.df['uzemi_txt'].unique()])
        years = sorted([int(y) for y in self.df['rok'].unique()])
        genders = ['Všechny'] + sorted([str(g) for g in self.df['POHLAVI_txt'].unique() if pd.notna(g)])
        stat_types = ['Průměr'] + sorted([str(s) for s in self.df['SPKVANTIL_txt'].unique() if pd.notna(s)])
        
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("📊 Czech Wage Statistics Dashboard", 
                           className="text-center mb-4 mt-4"),
                    html.P("Průměrná hrubá měsíční mzda a medián mezd v krajích (2011-2024)",
                          className="text-center text-muted mb-4")
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Region:", className="fw-bold"),
                    dcc.Dropdown(
                        id='region-filter',
                        options=[{'label': r, 'value': r} for r in regions],
                        value=[regions[0]],  # Default: first region
                        multi=True,
                        placeholder="Select regions..."
                    )
                ], md=6),
                
                dbc.Col([
                    html.Label("Gender:", className="fw-bold"),
                    dcc.Dropdown(
                        id='gender-filter',
                        options=[{'label': g, 'value': g} for g in genders],
                        value='Všechny',
                        placeholder="Select gender..."
                    )
                ], md=3),
                
                dbc.Col([
                    html.Label("Statistics:", className="fw-bold"),
                    dcc.Dropdown(
                        id='stat-filter',
                        options=[{'label': s, 'value': s} for s in stat_types],
                        value='Průměr',
                        placeholder="Select stat type..."
                    )
                ], md=3),
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Year Range:", className="fw-bold"),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=min(years),
                        max=max(years),
                        value=[min(years), max(years)],
                        marks={year: str(year) for year in years[::2]},  # Every 2nd year
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], md=12)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='time-series-chart', style={'height': '500px'})
                ], md=12)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='bar-chart', style={'height': '400px'})
                ], md=6),
                
                dbc.Col([
                    html.Div(id='stats-summary', className="p-3 border rounded bg-light")
                ], md=6)
            ])
            
        ], fluid=True)
        
        @self.app.callback(
            [Output('time-series-chart', 'figure'),
             Output('bar-chart', 'figure'),
             Output('stats-summary', 'children')],
            [Input('region-filter', 'value'),
             Input('gender-filter', 'value'),
             Input('stat-filter', 'value'),
             Input('year-slider', 'value')]
        )
        def update_charts(regions, gender, stat_type, year_range):
            df_filtered = self.df.copy()          
            year_range = [int(year_range[0]), int(year_range[1])]  

            if regions:
                df_filtered = df_filtered[df_filtered['uzemi_txt'].isin(regions)]
            
            if gender == 'Všechny':
                df_filtered = df_filtered[df_filtered['POHLAVI_txt'].isna()]
            else:
                df_filtered = df_filtered[df_filtered['POHLAVI_txt'] == gender]
            
            if stat_type == 'Průměr':
                df_filtered = df_filtered[df_filtered['SPKVANTIL_txt'].isna()]
            else:
                df_filtered = df_filtered[df_filtered['SPKVANTIL_txt'] == stat_type]
            
            df_filtered = df_filtered[
                (df_filtered['rok'] >= year_range[0]) & 
                (df_filtered['rok'] <= year_range[1])
            ].copy()
            
            df_filtered['rok'] = df_filtered['rok'].astype(int)
            df_filtered['hodnota'] = df_filtered['hodnota'].astype(float)
            
            fig_ts = px.line(
                df_filtered,
                x='rok',
                y='hodnota',
                color='uzemi_txt',
                markers=True,
                title='Wage Trends Over Time',
                labels={'rok': 'Year', 'hodnota': 'Wage (CZK)', 'uzemi_txt': 'Region'}
            )
            fig_ts.update_layout(
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            latest_year = int(df_filtered['rok'].max())
            df_latest = df_filtered[df_filtered['rok'] == latest_year].copy()
            df_latest = df_latest.sort_values('hodnota', ascending=True)
            
            fig_bar = px.bar(
                df_latest,
                x='hodnota',
                y='uzemi_txt',
                orientation='h',
                title=f'Wages in {latest_year}',
                labels={'hodnota': 'Wage (CZK)', 'uzemi_txt': 'Region'},
                color='hodnota',
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(showlegend=False)
            
            if len(df_filtered) > 0:
                avg_wage = float(df_filtered['hodnota'].mean())
                min_wage = float(df_filtered['hodnota'].min())
                max_wage = float(df_filtered['hodnota'].max())
                growth = None
                
                if len(df_filtered['rok'].unique()) > 1:
                    first_year = int(df_filtered['rok'].min())
                    last_year = int(df_filtered['rok'].max())
                    first_val = float(df_filtered[df_filtered['rok'] == first_year]['hodnota'].mean())
                    last_val = float(df_filtered[df_filtered['rok'] == last_year]['hodnota'].mean())
                    growth = ((last_val - first_val) / first_val) * 100
                
                summary = html.Div([
                    html.H4("📈 Statistics Summary", className="mb-3"),
                    html.Hr(),
                    html.P([html.Strong("Average Wage: "), f"{avg_wage:,.0f} CZK"]),
                    html.P([html.Strong("Minimum: "), f"{min_wage:,.0f} CZK"]),
                    html.P([html.Strong("Maximum: "), f"{max_wage:,.0f} CZK"]),
                    html.P([html.Strong("Data Points: "), f"{len(df_filtered)}"]),
                    html.Hr(),
                    html.P([
                        html.Strong("Growth: "),
                        f"{growth:+.1f}%" if growth else "N/A",
                        html.Br(),
                        html.Small(f"({year_range[0]} → {year_range[1]})", className="text-muted")
                    ]) if growth else html.Div()
                ])
            else:
                summary = html.Div([
                    html.H4("⚠️ No Data", className="text-warning"),
                    html.P("No data matches the selected filters.")
                ])
            
            return fig_ts, fig_bar, summary
    
    def run(self, debug=True, port=8050):
        if self.app is None:
            print("App not created. Call create_app() first.")
            return
        
        print(f"\n{'='*60}")
        print("🚀 Starting Dash Application")
        print(f"{'='*60}")
        print(f"Dashboard URL: http://127.0.0.1:{port}/")
        print("Press Ctrl+C to stop the server")
        print(f"{'='*60}\n")
        
        self.app.run(debug=debug, port=port)


def main():
    dashboard = CZSODashApp(dataset_id='110080')   
    if not dashboard.fetch_data():
        print("Failed to fetch data!")
        return   
    dashboard.create_app()
    dashboard.run(debug=True, port=8050)

if __name__ == "__main__":
    main()