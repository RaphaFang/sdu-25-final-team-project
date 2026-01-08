import pandas as pd
from IPython.display import display
import missingno as msno
import plotly.express as px

def nikolaos_func(cleaned_data_route, region_data_route):
    # 1. Load datasets
    life_df = pd.read_csv("/Users/fangsiyu/Desktop/intro_pj/life_cleaned.csv")
    region_df = pd.read_csv("/Users/fangsiyu/Desktop/intro_pj/country_continent.csv")
    # 1. Merge the two datasets
    merged_df = pd.merge(life_df, region_df, on="name", how="left")
    # 1. Identify year columns
    year_cols = [
                col for col in merged_df.columns # loops over every column name
                if col.isdigit() # filter condition
                ]

    # 2. Tranform them by using `melt`
    long_df = pd.melt(
        merged_df, 
        id_vars=['geo', 'name', 'Continent'],  # keep these columns the same
        value_vars=year_cols, # transform these columns
        var_name='Year', # this column will store the previous column names
        value_name='Life_Exp' # this column will contain the corresponding values
        )
    long_df['Year'] = long_df['Year'].astype(int)
    long_df = long_df.dropna(subset=['Continent', 'Life_Exp'])
    # Calculate continent averages per year per Continent
    continent_trends = (
        long_df.groupby(['Continent', 'Year'])['Life_Exp'].mean() # Calculate the average life expectancy for each continent-year pair
        .reset_index() # Turns the new data to columns
        .rename(columns={'Life_Exp': 'Avg_Life_Exp'})
    )
    #====================================================#
    # Filter for years. Used to focus on the range we want
    line_data = continent_trends[
        (continent_trends['Year'] >= 1900) &
        (continent_trends['Year'] <= 2026) ]
    #====================================================#


    # Create plot
    fig = px.line(
        line_data, 
        x="Year", 
        y="Avg_Life_Exp", 
        color="Continent",
        title="Life Expectancy Trend by Continent",
        labels={"Year": "Year", "Avg_Life_Exp": "Average Life Expectancy"},
        template="plotly_white"
    )

    fig.show()