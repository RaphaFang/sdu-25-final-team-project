import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import modules.sabbir_analysis.data_modelling as dm
import modules.sabbir_analysis.analysis_rq1 as vis_rq1

import modules.siyu_analysis.core_func as siyu_core
import modules.siyu_analysis.plotly_vis as siyu_vis


def main_dash_app(cleaned_data_route):
    df_cleaned = pd.read_csv(cleaned_data_route)
    n_countries = len(df_cleaned)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container(
        [
            html.H1("Life Expectancy Analysis Dashboard", className="text-center my-4"),

            html.H4("Sabbir, How long does it take countries to increase their life expectancy across a user-selected interval, and which countries achieve this improvement the fastest or slowest?", className="mt-4"),

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

            dbc.Row(dbc.Col(dcc.Graph(id="rq1-plot"), width=12)),

            html.H3("Si-Yu, Life Expectancy Anomaly Analysis", className="mt-5"),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="anomaly-type",
                            options=[
                                {"label": "Short-term anomaly", "value": "short"},
                                {"label": "Long-term anomaly", "value": "long"},
                            ],
                            value="short",
                            clearable=False,
                        ),
                        width=4
                    ),
                    dbc.Col(
                        dcc.RadioItems(
                            id="anomaly-dimension",
                            options=[
                                {"label": "By Year", "value": "year"},
                                {"label": "By Country (Top 20)", "value": "country"},
                            ],
                            value="year",
                            inline=True
                        ),
                        width=8
                    ),
                ],
                className="mb-3"
            ),

            dbc.Row(dbc.Col(dcc.Graph(id="siyu-anomaly-plot"), width=12)),

            html.H4("Si-Yu, Inspect each country by ID", className="mt-4"),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Country index"),
                            dcc.Slider(
                                id="country-index",
                                min=0,
                                max=n_countries - 1,
                                step=1,
                                value=0,
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ],
                        width=12
                    )
                ],
                className="mb-2"
            ),

            dbc.Row(dbc.Col(dcc.Graph(id="country-inspector-plot"), width=12)),
        ],
        fluid=True
    )
# callback =========================================================================================================
    @app.callback(
        Output("rq1-plot", "figure"),
        Input("life-exp-interval", "value")
    )
    def update_rq1_plot(interval):
        lower, upper = interval
        if lower >= upper:
            return {}

        df_result = dm.compute_time_to_reach_interval(df_cleaned, lower, upper)
        if df_result.empty:
            return {}

        return vis_rq1.plot_fastest_slowest_countries(df_result, top_n=5)

    @app.callback(
        Output("siyu-anomaly-plot", "figure"),
        Input("anomaly-type", "value"),
        Input("anomaly-dimension", "value"),
    )
    def update_siyu_overview(anomaly_type, dim):
        data = siyu_core.compute_anomaly_core(cleaned_data_route)
        z_df = data["z_short"] if anomaly_type == "short" else data["z_long"]

        if dim == "year":
            series = siyu_core.anomaly_count_by_year(z_df)
            return siyu_vis.plot_anomaly_by_year(
                series,
                data["years"],
                f"{anomaly_type.title()} Anomaly - Count by Year"
            )
        else:
            series = siyu_core.top_country_anomaly(z_df, top_n=20)
            index_to_country = data["df"]["name"].to_dict()
            return siyu_vis.plot_anomaly_by_country(
                series,
                index_to_country,
                f"{anomaly_type.title()} Anomaly - Top Countries"
            )

    @app.callback(
        Output("country-inspector-plot", "figure"),
        Input("country-index", "value"),
        Input("anomaly-type", "value"),
    )
    def update_country_inspector(country_index, anomaly_type):
        years, values, anomaly_years, country_name = siyu_core.country_inspector_data(
            cleaned_data_route,
            country_index=int(country_index),
            anomaly_type=anomaly_type,
            threshold=3
        )

        fig = siyu_vis.plot_country_inspector(
            years,
            values,
            anomaly_years,
            title=f"{country_name}_{country_index}: {anomaly_type.title()} anomaly marked with red dots"
        )

        # label = f"Current: {country_name} (index={country_index}) | anomalies: {len(anomaly_years)}"
        return fig

    return app