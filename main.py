from cleaning.utils import generate_cleaned_data

generate_cleaned_data("cleaning_process/life expected.csv", 
                        'cleaning_m/life_cleaned.csv',
                        machine_noise_floor=1e-12)