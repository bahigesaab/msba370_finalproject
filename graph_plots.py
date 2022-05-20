import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
import numpy as np


def plot_bar_chart(dataframe, x_column, y_column, title, orientation):

    bar_chart = px.bar(
        data_frame=dataframe,
        x=x_column,
        y=y_column,
        orientation=orientation,
        title=title,
        color_discrete_sequence=["#0083B8"]*len(dataframe)
    )

    # Format the chart
    bar_chart.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        xaxis_title=None,
        yaxis_title=None,
    )

    return bar_chart

##  Plotline Chart

def plot_line_chart(dataframe, x_column, y_column, title):
    df = dataframe.groupby(x_column, as_index=False)[[y_column]].sum()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df[x_column], y=df[y_column], mode='lines+markers'))

    fig.update_layout(
        {'title': title})
    fig.update_xaxes(tickformat="%b\n%Y")
    return fig

## KPI
def display_kpi(title, value, left_unit="", right_unit=""):
    container = st.container()
    with container:
        st.subheader(title)
        st.header(f'{left_unit} {value} {right_unit}')


def display_treemap(df, path1, path2, values,color):
    fig = px.treemap(df, path=[path1, path2], values=values,
                      color=color, hover_data=[values],
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df[color], weights=df[values]))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.show()


def display_world_map(df, title, latitude, longitude, coloring_theme, sizing_theme):
    mapbox_access_token = 'pk.eyJ1IjoiYmFoaWdlc2FhYiIsImEiOiJja3l5djA4czMwdzhoMnFxbDdqZXVhc2xjIn0.lqEdOX_HSMS4u-qNA6NXEQ'

    px.set_mapbox_access_token(mapbox_access_token)

    fig = px.scatter_mapbox(df,
                            lat=latitude,
                            lon=longitude,
                            color=coloring_theme,
                            size=sizing_theme,
                            zoom=1,
                            hover_data={'latitude':False, 'longitude':False,'Country':True, 'Region':False}
                            )

    fig.update_layout(title=title,
                      height=700,
                      legend=dict(orientation="h"))

    return fig


def display_usa_map(df, title, latitude, longitude, coloring_theme, sizing_theme):
    mapbox_access_token = 'pk.eyJ1IjoiYmFoaWdlc2FhYiIsImEiOiJja3l5djA4czMwdzhoMnFxbDdqZXVhc2xjIn0.lqEdOX_HSMS4u-qNA6NXEQ'

    px.set_mapbox_access_token(mapbox_access_token)

    fig = px.scatter_mapbox(df,
                            lat=latitude,
                            lon=longitude,
                            color=coloring_theme,
                            size=sizing_theme,
                            zoom=3.5,
                            hover_data={'latitude':False, 'longitude':False,'State':True, 'Region':False}
                            )

    fig.update_layout(title=title,
                      height=700,
                      mapbox=dict(
                          center=dict(
                              lat=38,
                              lon=-94
                          ),
                      ),
                      legend=dict(orientation="h"))

    return fig