from cleaning.utils import generate_cleaned_data
# from modules.si_yu import si_yu_plot, si_yu_func
from modules.si_yu import alert_func, country_inspector, si_yu_plot

df = generate_cleaned_data("cleaning/life expected.csv", 
                        'life_cleaned.csv',
                        machine_noise_floor=1e-12)

def whole_team(route, return_len: int = 10, country_index: int=0, L_or_S: str='short'):
    si_yu_plot(route)
    alert_package = alert_func(route, return_len)
    alert_year_for_country = country_inspector(route, country_index, L_or_S)

    return alert_package, alert_year_for_country

whole_team('life_cleaned.csv', return_len=10, country_index=1, L_or_S="long")