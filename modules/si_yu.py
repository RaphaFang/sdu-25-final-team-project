import pandas as pd
import matplotlib.pyplot as plt

def si_yu_plot(route):
    cleaned_df = pd.read_csv(route)
    index_country_dict = cleaned_df["name"].to_dict()
    years = list(cleaned_df.iloc[:, 4:].columns)

    df_1dif = cleaned_df.iloc[:, 4:].diff(axis=1)
    df_z = abs((df_1dif - df_1dif.mean()) / df_1dif.std())

    df_10ma = cleaned_df.iloc[:, 4:].rolling(window=10, axis=1).mean()
    df_10ma_diff = (cleaned_df.iloc[:, 4:] - df_10ma)
    df_z_10ma = abs((df_10ma_diff - df_10ma_diff.mean()) / df_10ma_diff.std())

    
    # p1 ------------------------------------------------------------------------------------------------
    series_short_flag_a0 = df_z[df_z > 3].notna().sum()
    plt.figure(figsize=(18,6))
    plt.plot(years, series_short_flag_a0.values)
    plt.xlabel("Year")
    plt.ylabel("Count of Countries")
    plt.title("Short-term anomaly, Count of Countries(Z-Score > 3sd)")
    plt.xticks(years[::10],rotation=45)
    plt.ylim(bottom=0)
    plt.grid()
    plt.savefig("figures/siyu_short_y", dpi=300, bbox_inches="tight")

    # p2 -----------------------------------------------------------------------------------------------
    series_short_flag_a1 = df_z[df_z > 3].notna().sum(axis=1).sort_values(ascending=False).head(20).to_dict()
    plt.figure(figsize=(18,6))

    for i, n in series_short_flag_a1.items():
        plt.bar((str(index_country_dict[i])+ '_' + str(i)), n, color="steelblue")

    plt.xlabel("Country")
    plt.ylabel("data count")
    plt.title("Short-term anomaly, Countries having the most anomalous count (Top 20)")
    plt.xticks(rotation=45)
    plt.savefig("figures/siyu_short_c", dpi=300, bbox_inches="tight")

    # p3 -----------------------------------------------------------------------------------------------
    series_long_flag_a0 = df_z_10ma[df_z_10ma > 3].notna().sum() # .sort_values(ascending=False)

    plt.figure(figsize=(18,6))
    plt.plot(years, series_long_flag_a0.values)

    plt.xlabel("Year")
    plt.ylabel("Count of Countries")
    plt.title("Long-term anomaly, Count of Countries(Z-Score > 3sd)")
    plt.xticks(years[::10],rotation=45)
    plt.ylim(bottom=0)
    plt.grid()
    plt.savefig("figures/siyu_long_y", dpi=300, bbox_inches="tight")

    # p4 -----------------------------------------------------------------------------------------------
    series_long_flag_a1 = df_z_10ma[df_z_10ma > 3].notna().sum(axis=1).sort_values(ascending=False).head(20).to_dict()

    plt.figure(figsize=(18,6))
    for i, n in series_long_flag_a1.items():
        plt.bar((str(index_country_dict[i]) + '_' + str(i)), n, color='steelblue')

    plt.xlabel("Country")
    plt.ylabel("data count")
    plt.title("Long-term anomaly, Countries having the most anomalous count (Top 20)")
    plt.xticks(rotation=45)
    plt.savefig("figures/siyu_long_c", dpi=300, bbox_inches="tight")


def alert_func(route, return_len: int = 10):
    cleaned_df = pd.read_csv(route)
    index_country_dict = cleaned_df["name"].to_dict()

    df_1dif = cleaned_df.iloc[:, 4:].diff(axis=1)
    df_z = abs((df_1dif - df_1dif.mean()) / df_1dif.std())

    df_10ma = cleaned_df.iloc[:, 4:].rolling(window=10, axis=1).mean()
    df_10ma_diff = (cleaned_df.iloc[:, 4:] - df_10ma)
    df_z_10ma = abs((df_10ma_diff - df_10ma_diff.mean()) / df_10ma_diff.std())

    dd = {}

    series_short_flag_a0 = df_z[df_z > 3].notna().sum().sort_values(ascending=False).head(return_len).index.to_list()
    series_short_flag_a1 = df_z[df_z > 3].notna().sum(axis=1).sort_values(ascending=False).head(return_len).index.to_list()

    series_long_flag_a0 = df_z_10ma[df_z_10ma > 3].notna().sum().sort_values(ascending=False).head(return_len).index.to_list()
    series_long_flag_a1 = df_z_10ma[df_z_10ma > 3].notna().sum(axis=1).sort_values(ascending=False).head(return_len).index.to_list()

    dd["index_to_country"] = index_country_dict

    dd["short_country"] = series_short_flag_a1
    dd["short_year"] = series_short_flag_a0

    dd["long_country"] = series_long_flag_a1
    dd["long_year"] = series_long_flag_a0

    return dd

def country_inspector(route, country_index: int=0, L_or_S: str='short'):
    if L_or_S not in ["short", 'long']:
        return "You can onl put short or long at parameter L_or_S"
    
    cleaned_df = pd.read_csv(route)
    years = list(cleaned_df.iloc[:, 4:].columns)

    df_1dif = cleaned_df.iloc[:, 4:].diff(axis=1)
    df_z = abs((df_1dif - df_1dif.mean()) / df_1dif.std())

    df_10ma = cleaned_df.iloc[:, 4:].rolling(window=10, axis=1).mean()
    df_10ma_diff = (cleaned_df.iloc[:, 4:] - df_10ma)
    df_z_10ma = abs((df_10ma_diff - df_10ma_diff.mean()) / df_10ma_diff.std())


    
    target = cleaned_df.iloc[country_index, 4:]

    if L_or_S == "short":
        df_target_i = df_z[df_z > 3].iloc[country_index]
    
    elif L_or_S == "long":
        df_target_i = df_z_10ma[df_z_10ma > 3].iloc[country_index]
    
    plt.figure(figsize=(18, 6))
    plt.plot(years, target.values)

    plt.fill_between(df_target_i.index, 0, 100, 
                    where=(df_target_i.notna()), 
                    color='red', alpha=0.2)

    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.title(f"Life Expected, with {L_or_S} Anomaly Sequence Marked")
    plt.xticks(years[::10],rotation=45)
    plt.ylim(bottom=0)
    plt.grid()
    plt.savefig(f"figures/siyu_{country_index}_plot", dpi=300, bbox_inches="tight")

    return df_target_i[df_target_i.notna()].index.to_list()


if __name__ == "__main__":
    si_yu_plot("modules/life_cleaned.csv")
    
    catch_1 = alert_func("life_cleaned.csv",return_len= 20)
    print(catch_1)

    catch_2 = country_inspector("life_cleaned.csv", 0, 'long')
    print(catch_2)



