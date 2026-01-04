import pandas as pd

def generate_cleaned_data(row_data_route, cleaned_data_route, machine_noise_floor=1e-12):
    df = pd.read_csv(row_data_route)
    
    drop_list = [3, 46, 92, 100, 107, 112, 131, 138, 156, 178]
    df_dropped = df.drop(index=drop_list)
    # print("df_dropped.shape[0]:",df_dropped.shape[0], ", df.shape[0]:",df.shape[0])
    assert (df_dropped.shape[0] == 184 and df.shape[0] == 194), "Error, either drop_list or df len is different from original."

    df_acceleration = df_dropped.iloc[:, 2:].diff(axis=1).diff(axis=1).abs()

    vals = df_acceleration.stack()
    scale = vals[vals > machine_noise_floor].quantile(0.001)
    print(f"We got scale: {scale}")
    series_non_l_count = (df_acceleration > scale).sum(axis=1)
    series_non_l_ratio = series_non_l_count / len(df.columns[2:])

    df_dropped.insert(2, 'non_linearity_ratio', series_non_l_ratio)
    df_dropped.insert(2, 'non_linearity_count', series_non_l_count)    
    # print(df_dropped.head(10))

    df_dropped.to_csv(cleaned_data_route, index=False)


if __name__ == "__main__":
    generate_cleaned_data("cleaning_process/life expected.csv", 
                          'cleaning_m/life_cleaned.csv',
                          machine_noise_floor=1e-12)