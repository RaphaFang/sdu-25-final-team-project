import plotly.graph_objects as go

def plot_anomaly_by_year(series, years, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=series.values, mode="lines+markers", name="Count"))

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Count of Countries",
        template="plotly_white",
        height=520,
        margin=dict(b=110),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=years[::10],
        ticktext=years[::10],
        tickangle=45
    )
    return fig


def plot_anomaly_by_country(series, index_to_country, title):
    labels = [f"{index_to_country[i]}_{i}" for i in series.index]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=series.values, name="Anomaly Count"))

    fig.update_layout(
        title=title,
        xaxis_title="Country",
        yaxis_title="Anomaly Count",
        template="plotly_white",
        height=520,
    )
    return fig


def plot_country_inspector(years, values, anomaly_years, title):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=years,
            y=values,
            mode="lines",
            name="Life Expectancy",
        )
    )

    if anomaly_years:
        year_to_value = {y: v for y, v in zip(years, values)}
        xs = anomaly_years
        ys = [year_to_value.get(y) for y in xs]

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers",
                name="Anomaly",
                marker=dict(color="red", size=9),
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Life Expectancy",
        template="plotly_white",
        height=520,
        margin=dict(b=110),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=years[::10],
        ticktext=years[::10],
        tickangle=45
    )

    return fig