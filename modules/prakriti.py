import pandas as pd
import matplotlib.pyplot as plt

def prakriti_func(route):
    # Loading the dataset
    df = pd.read_csv(route)

    # Create a list of years from 1800 to 2020
    years = [str(y) for y in range(1800, 2021)]

    # Keep only the columns we need: country name + the years
    df_selected = df[["name"] + years].copy()

    # Convert the year columns to numbers (invalid values become NaN)
    df_selected[years] = df_selected[years].apply(pd.to_numeric, errors="coerce")


    gap_list = []

    for year in years:
        highest = df_selected[year].max()
        lowest = df_selected[year].min()
        gap = highest - lowest
        gap_list.append([int(year), gap])

    # Turn the list into a dataframe
    gap_df = pd.DataFrame(gap_list, columns=["Year", "Gap"])

    # y-axis limit
    max_gap = gap_df["Gap"].max()
    top = int((max_gap // 5 + 1) * 5)

    # Plot the gap over time
    plt.figure(figsize=(18, 6))
    plt.plot(gap_df["Year"], gap_df["Gap"])

    plt.title("Life Expectancy Inequality Gap (1800–2020)")
    plt.xlabel("Year")
    plt.ylabel("Gap (years)")

    plt.ylim(0, top)
    plt.yticks(range(0, top + 1, 5))
    plt.xticks(range(1800, 2021, 20))
    plt.grid(True)

    plt.savefig(f"figures/prakriti_plot", dpi=300, bbox_inches="tight")

