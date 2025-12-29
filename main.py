from cleaning.utils import generate_cleaned_data
from modules.si_yu import alert_func, country_inspector, si_yu_plot
from modules.prakriti import prakriti_func

row_data_route = "cleaning/life expected.csv"
cleaned_data_route = 'life_cleaned.csv'

generate_cleaned_data(row_data_route, 
                        cleaned_data_route,
                        machine_noise_floor=1e-12)

def whole_team(cleaned_data_route, return_len: int = 10, country_index: int=0, L_or_S: str='short'):
    si_yu_plot(cleaned_data_route)
    alert_package = alert_func(cleaned_data_route, return_len)
    alert_year_for_country = country_inspector(cleaned_data_route, country_index, L_or_S)

    prakriti_func(route)

    return alert_package, alert_year_for_country

whole_team(cleaned_data_route, return_len=10, country_index=1, L_or_S="long")