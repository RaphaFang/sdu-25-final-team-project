import pandas as pd
import plotly.express as px


def modeling(df,country_code):
    country_df = df[df['geo_data'] == country_code]

    # Getting only the nessasary values
    life_cols = df.columns[2:-2]
    life_data = country_df[life_cols]

    # Getting the numeric values
    all_values = life_data.values.flatten()
    all_values = all_values.round(0)

    # Count all values
    value_counts = pd.Series(all_values).value_counts().reset_index()
    value_counts.columns = ['Life Expectancy', 'Count']
    value_counts = value_counts.sort_values('Life Expectancy')

    return value_counts

def ploting(df, country_code):

    # Plot
    fig = px.bar(
        df,
        x='Life Expectancy',
        y='Count',
        title=f'Life Expectancy Distribution - {country_code}',
        labels={'Count': 'Number of Occurrences', 'Life Expectancy': 'Years of Life'},
        color_discrete_sequence=['steelblue']
    )

    return fig
