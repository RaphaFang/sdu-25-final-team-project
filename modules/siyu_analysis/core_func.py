import pandas as pd

def compute_anomaly_core(route):
    df = pd.read_csv(route)
    years = list(df.iloc[:, 4:].columns)
    df_val = df.iloc[:, 4:]

    df_1diff = df_val.diff(axis=1)
    z_short = abs((df_1diff - df_1diff.mean()) / df_1diff.std())

    df_10ma = df_val.T.rolling(window=10).mean().T
    df_10ma_diff = df_val - df_10ma
    z_long = abs((df_10ma_diff - df_10ma_diff.mean()) / df_10ma_diff.std())

    return {
        "df": df,
        "years": years,
        "z_short": z_short,
        "z_long": z_long,
    }

def anomaly_count_by_year(z_df, threshold=3):
    return z_df[z_df > threshold].notna().sum(axis=0)

def anomaly_count_by_country(z_df, threshold=3):
    return z_df[z_df > threshold].notna().sum(axis=1)

def top_country_anomaly(z_df, threshold=3, top_n=20):
    return (
        anomaly_count_by_country(z_df, threshold)
        .sort_values(ascending=False)
        .head(top_n)
    )

def country_inspector_data(route, country_index: int = 0, anomaly_type: str = "short", threshold: float = 3):
    if anomaly_type not in ("short", "long"):
        raise ValueError("anomaly_type must be 'short' or 'long'")

    data = compute_anomaly_core(route)
    df = data["df"]
    years = data["years"]

    values_series = df.iloc[country_index, 4:]
    values = values_series.values.tolist()

    z_df = data["z_short"] if anomaly_type == "short" else data["z_long"]

    z_row = z_df.iloc[country_index]
    anomaly_mask = (z_row > threshold) & z_row.notna()
    anomaly_years = z_row.index[anomaly_mask].tolist()

    country_name = str(df.loc[country_index, "name"])

    return years, values, anomaly_years, country_name