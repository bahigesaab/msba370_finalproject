import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from clustering_functions import elbow_function, plot_cluster, clusters_centroid_dataframe
from get_data import get_data_from_csv


def clustering_page():

    st.title("Clustering Transactions per Discount, Sales and Profit")
    sales = get_data_from_csv()


    def options_list(column):
        sales_list = np.sort(sales[column].unique())
        sales_list = np.insert(sales_list, 0, ["All"])
        return sales_list


    def selection_box(column):
        selected_option = st.selectbox(
            f'Select {column}:',
            options=options_list(column),
        )
        if selected_option == "All":
            selected_option = [i for i in options_list(column)]

        return selected_option


    country_cell, state_cell = st.columns(2)

    with country_cell:
        country = selection_box("Country")


    sales_countries =  sales.query("Country==@country")

    sales_discount_subset = sales_countries[["Discount", "Sales", "Profit"]]

    with st.container():
         st.header("Elbow Curve")
         elbow_fig = elbow_function(sales_discount_subset)
         st.pyplot(elbow_fig)


    selected_clusters = st.selectbox(
        'Select the number of clusters:',
        options=range(1,10)
    )

    with st.container():
        st.header("3D Clusters Graph")
        clusters_fig = plot_cluster(sales_discount_subset, selected_clusters)
        st.plotly_chart(clusters_fig)

