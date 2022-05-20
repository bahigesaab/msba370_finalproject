import streamlit as st
import pandas as pd
import numpy as np

from get_data import get_usa_data_from_csv, divide
from graph_plots import plot_bar_chart, plot_line_chart, display_kpi, display_world_map, display_usa_map


def usa_profit_analytics():

    st.title("US Profit Analytics")
    sales = get_usa_data_from_csv()
    states = pd.read_csv("states.csv")

    sales_states = pd.merge(sales, states, on='State')

    def options_list(df, column):
        sales_list = np.sort(df[column].unique())
        sales_list = np.insert(sales_list, 0, ["All"])
        return sales_list

    def selection_box(df, column):
        selected_option = st.selectbox(
            f'Select {column}:',
            options=options_list(df, column),
        )
        if selected_option == "All":
            selected_option = [i for i in options_list(df, column)]

        return selected_option

    segment_cell, region_cell, country_cell, category_cell, subcategory_cell, product_cell = st.columns(6)

    with segment_cell:
        customer_segment = selection_box(sales_states, "Segment")

    sales_by_segment = sales_states.query("Segment==@customer_segment")

    with region_cell:
        region = selection_box(sales_by_segment, "Region")

    sales_by_region = sales_by_segment.query("Region==@region")

    with country_cell:
        state = selection_box(sales_by_region, "State")

    with category_cell:
        category = selection_box(sales_by_region, "Category")

    sales_by_category = sales_by_region.query("Category==@category")

    with subcategory_cell:
        subcategory = selection_box(sales_by_category, "Subcategory")

    sales_by_subcategory = sales_by_category.query("Subcategory==@subcategory")

    with product_cell:
        product_name = selection_box(sales_by_subcategory, "Product")

    sales_by_product = sales_by_subcategory.query("Product==@product_name")

    sales_queried = sales_states.query(
        "Segment==@customer_segment & Region==@region & State==@state"\
        "& Product==@product_name & Category==@category & Subcategory==@subcategory"
    )

    KPI_1, KPI_2, KPI_3 = st.columns(3)

    with KPI_1:
        total_sales = int(sales_queried["Profit"].sum())
        display_kpi("Total Profit", "{:,}".format(total_sales),"$")

    with KPI_2:
        average_sales_per_transaction = round(sales_queried["Profit"].mean(),2)
        display_kpi("Average Profit per Transaction", "{:,}".format(average_sales_per_transaction), "$")

    with KPI_3:
        total_sales = int(sales_queried["Profit"].sum())
        months_number = len(sales_queried["Month_Year"].unique())
        average_sales_per_month = round(divide(total_sales, months_number),2)

        display_kpi("Average Profit per Month", "{:,}".format(average_sales_per_month), "$")

    category_column, subcategory_column = st.columns(2)

    sales_category = sales_queried.groupby(by=["Category"]).sum()[["Profit"]].sort_values(by=["Profit"])

    with category_column:
        category_horizontal_barchart = plot_bar_chart(sales_category,
                                                                "Profit",
                                                                sales_category.index,
                                                                "<b> Profit by Category</b>",
                                                                "h")
        st.plotly_chart(category_horizontal_barchart)

    sales_subcategory = sales_queried.groupby(by=["Subcategory"]).sum()[["Profit"]].sort_values(by=["Profit"])

    with subcategory_column:
        subcategory_horizontal_barchart = plot_bar_chart(sales_subcategory,
                                                                "Profit",
                                                                sales_subcategory.index,
                                                                "<b> Profit by Subcategory</b>",
                                                                 "h")
        st.plotly_chart(subcategory_horizontal_barchart)



    with st.container():
        line_chart = plot_line_chart(sales_queried, "Month_Year", "Profit", "<b>Profit by Month($)<b>")
        st.plotly_chart(line_chart, use_container_width=True)


    with st.container():
        map_lat = sales_queried.latitude
        map_long = sales_queried.longitude
        map_color = sales_queried.Region
        sales_queried = sales_queried.set_index('Profit')

        map = display_usa_map(sales_queried, "<b>Profit per State($)</b>", map_lat, map_long, map_color, np.absolute((sales_queried.index)))
        st.plotly_chart(map, use_container_width=True)



    st.markdown(
        """
        <style>
        .css-1idizjf, .css-zi8otl{
            border: 1px solid;
            text-align: center;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )