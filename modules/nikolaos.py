import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio

def nikolaos_func(cleaned_data_route, region_data_route):
    # 1. Load data
    life_df = pd.read_csv(cleaned_data_route)
    region_df = pd.read_csv(region_data_route)

    # 2. Join Continent Data and Clean
    merged_df = pd.merge(life_df, region_df, on="name", how="left")
    merged_df['geo'] = merged_df['geo'].str.upper()

    # Identify year columns
    year_cols = [col for col in merged_df.columns if col.isdigit()]

    # Reshape to Long Format
    long_df = pd.melt(
        merged_df, 
        id_vars=['geo', 'name', 'Continent'], 
        value_vars=year_cols, 
        var_name='Year', 
        value_name='Life_Exp'
        )

    long_df['Year'] = long_df['Year'].astype(int)
    long_df['Life_Exp'] = pd.to_numeric(long_df['Life_Exp'], errors='coerce')

    # Filter 5-year blocks and drop missing continents
    long_df = long_df.dropna(subset=['Continent', 'Life_Exp'])
    long_df['Display_Year'] = (long_df['Year'] // 5) * 5

    # 3. Calculate Continent Averages per 5-Year Block
    continent_trends = long_df.groupby(['Continent', 'Display_Year'])['Life_Exp'].mean().reset_index()
    continent_trends = continent_trends.rename(columns={'Life_Exp': 'Avg_Life_Exp'})

    # 4. Prepare Map Data (we need every country to have its continent's average)
    map_data = pd.merge(
        long_df[['geo', 'Continent']].drop_duplicates(), 
        continent_trends, 
        on='Continent'
    )

    line_data = continent_trends

    # 3. Create the Base Line Plot
    # We create a line for every continent that stays visible
    fig = px.line(
        line_data, 
        x="Display_Year", 
        y="Avg_Life_Exp", 
        color="Continent",
        title="Life Expectancy Trend by Continent (1800 - 2100)",
        labels={"Display_Year": "Year", "Avg_Life_Exp": "Average Life Expectancy"},
        template="plotly_white"
    )

    # 4. Add the "Moving Tracker" (Points that follow the slider)
    years = sorted(line_data['Display_Year'].unique())
    initial_year = years[0]

    marker_start = len(fig.data)

    # Add a scatter trace for the 'current' points
    for continent in line_data['Continent'].unique():
        cont_data = line_data[
            (line_data['Continent'] == continent) & 
            (line_data['Display_Year'] == initial_year)
        ]
        fig.add_trace(
            go.Scatter(
                x=cont_data['Display_Year'],
                y=cont_data['Avg_Life_Exp'],
                mode='markers+text',
                marker=dict(size=12, line=dict(width=2, color='White')),
                text=cont_data['Avg_Life_Exp'],
                textposition="top center",
                name=f"Current {continent}",
                showlegend=False
            )
        )

    # 5. Create Frames for the Slider
    frames = []
    continents = line_data['Continent'].unique()

    for yr in years:
        frame_data = []
        curr_yr_data = line_data[line_data['Display_Year'] == yr]
        
        for continent in continents:
            cont_yr_data = curr_yr_data[curr_yr_data['Continent'] == continent]
            frame_data.append(
                go.Scatter(
                    x=cont_yr_data['Display_Year'],
                    y=cont_yr_data['Avg_Life_Exp'],
                    text=cont_yr_data['Avg_Life_Exp']
                )
            )
        
        frames.append(
            go.Frame(
                data=frame_data,
                name=str(yr),
                traces=list(range(marker_start, marker_start + len(continents)))
            )
        )

    fig.frames = frames

    # 6. Slider and Layout
    fig.update_layout(
        xaxis=dict(range=[1790, 2110]),
        yaxis=dict(range=[20, 95]),
        updatemenus=[{"buttons": [{"args": [None, {"frame": {"duration": 100, "redraw": False}}], "label": "Play", "method": "animate"}],
                    "type": "buttons", "x": 0.1, "y": -0.2}],
        sliders=[{"steps": [{"args": [[str(yr)], {"frame": {"duration": 100, "redraw": False}, "mode": "immediate"}],
                            "label": str(yr), "method": "animate"} for yr in years],
                "x": 0.2, "len": 0.8, "y": -0.2}]
    )

    pio.renderers.default = 'iframe'
    fig.show()