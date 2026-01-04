import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import modules.sabbir_analysis.data_modelling as dm
import modules.sabbir_analysis.analysis_rq1 as vis_rq1
import pandas as pd

def sabbir_dash_app(cleaned_data_route):
    # Load data
    df_cleaned = pd.read_csv(cleaned_data_route)

    # Initialize Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container(
        [
            html.H1(
                "How long does it take countries to increase their life expectancy across a user-selected interval, and which countries achieve this improvement the fastest or slowest?",
                className="text-center my-4"
            ),

            # Interval slider 
            dbc.Row(
                dbc.Col(
                    [
                        html.Label("Life Expectancy Interval (years)"),
                        dcc.RangeSlider(
                            id="life-exp-interval",
                            min=30,
                            max=90,
                            step=1,
                            value=[40, 70],
                            marks={i: str(i) for i in range(30, 91, 10)},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    width=12
                ),
                className="mb-4"
            ),

            dbc.Row(
                dbc.Col(
                    dcc.Graph(id="rq1-plot"),
                    width=12
                )
            ),
        ],
        fluid=True
    )


    @app.callback(
        Output("rq1-plot", "figure"),
        Input("life-exp-interval", "value")
    )
    def update_plot(interval):
        lower, upper = interval
        if lower >= upper:
            return {}

        df_result = dm.compute_time_to_reach_interval(df_cleaned, lower, upper)
        if df_result.empty:
            return {}

        return vis_rq1.plot_fastest_slowest_countries(df_result, top_n=5)
    
    return app

# if __name__ == "__main__":
#     app.run(debug=True)