import pandas as pd

def compute_time_to_reach_interval(df, lower, upper):
    """
    Compute the number of years each country takes to go from `lower` to `upper` life expectancy.
    Returns a DataFrame with columns: ['geo', 'name', 'start_year', 'end_year', 'duration']
    """
    results = []

    years = df.columns[4:].astype(int)

    for idx, row in df.iterrows():
        life_values = row[4:].values
        # Find first year ≥ lower threshold
        lower_year_idx = next((i for i, v in enumerate(life_values) if v >= lower), None)
        # Find first year ≥ upper threshold after lower_year_idx
        upper_year_idx = next((i for i, v in enumerate(life_values) if v >= upper and i >= lower_year_idx), None) if lower_year_idx is not None else None

        if lower_year_idx is not None and upper_year_idx is not None:
            start_year = years[lower_year_idx]
            end_year = years[upper_year_idx]
            duration = end_year - start_year
            results.append({
                'geo': row['geo'],
                'name': row['name'],
                'start_year': start_year,
                'end_year': end_year,
                'duration': duration
            })

    df_result = pd.DataFrame(results)
    return df_result