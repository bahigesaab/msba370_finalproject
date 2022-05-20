import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu


from usa_profit_analytics import usa_profit_analytics
from usa_sales_analytics import usa_sales_analytics
from clustering_page import clustering_page
from world_profit_analytics import world_profit_analytics
from world_sales_analytics import world_sales_analytics

st.set_page_config(page_title="Global Sales Analytics Dashboard",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide")

sales = pd.read_csv('Sales_Data.csv', encoding='ISO-8859-1')

with st.sidebar:
    choose = option_menu("Dashboards", ["World Sales", "World Profit", "US Sales", "US Profit", "Clustering Transactions"],
                         icons=['file-bar-graph', 'file-earmark-bar-graph', 'graph-up', 'graph-up-arrow','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "World Sales":
    world_sales_analytics()

elif choose == "World Profit":
    world_profit_analytics()

elif choose == "US Sales":
    usa_sales_analytics()

elif choose == "US Profit":
    usa_profit_analytics()

elif choose == "Clustering Transactions":
    clustering_page()


# https://plotly.com/python/styling-plotly-express/
# https://www.youtube.com/watch?v=tWFQqaRtSQA