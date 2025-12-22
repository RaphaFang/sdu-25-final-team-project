from cleaning.utils import generate_cleaned_data
from modules.main import group_modules

df = generate_cleaned_data("cleaning/life expected.csv", 
                        'modules/life_cleaned.csv',
                        machine_noise_floor=1e-12)

temp = group_modules(df)
