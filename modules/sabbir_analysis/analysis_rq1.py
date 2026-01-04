import plotly.graph_objs as go

def plot_fastest_slowest_countries(df_result, top_n=5):
    """
    Plot fastest and slowest countries to reach the given life expectancy interval.
    """
    df_fastest = df_result.nsmallest(top_n, 'duration')
    df_slowest = df_result.nlargest(top_n, 'duration')

    fig = go.Figure()

    # Fastest countries (green)
    fig.add_trace(go.Bar(
        x=df_fastest['name'],
        y=df_fastest['duration'],
        name='Fastest',
        marker_color='green'
    ))

    # Slowest countries (red)
    fig.add_trace(go.Bar(
        x=df_slowest['name'],
        y=df_slowest['duration'],
        name='Slowest',
        marker_color='red'
    ))

    fig.update_layout(
        title=f"Top {top_n} Fastest and Slowest Countries to Reach Interval",
        xaxis_title="Country",
        yaxis_title="Duration (years)",
        barmode='group',
        template='plotly_white'
    )

    return fig