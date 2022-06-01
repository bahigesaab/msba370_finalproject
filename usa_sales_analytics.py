import streamlit as st
import pandas as pd
import numpy as np

from get_data import get_usa_data_from_csv, divide
from graph_plots import plot_bar_chart, plot_line_chart, display_kpi, display_world_map, display_usa_map


def usa_sales_analytics():

    st.title("US Sales Analytics")
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

    KPI_1, KPI_2, KPI_3, KPI_4, KPI_5 = st.columns(5)

    with KPI_1:
        total_sales = int(sales_queried["Sales"].sum())
        display_kpi("Total Sales", "{:,}".format(total_sales),"$")

    with KPI_2:
        average_sales_per_transaction = round(sales_queried["Sales"].mean(),2)
        display_kpi("Sales per Transaction", "{:,}".format(average_sales_per_transaction), "$")

    with KPI_3:
        total_sales = int(sales_queried["Sales"].sum())
        months_number = len(sales_queried["Month_Year"].unique())
        average_sales_per_month = round(divide(total_sales, months_number),2)
        display_kpi("Mean Sales per Month", "{:,}".format(average_sales_per_month), "$")

    with KPI_4:
        total_customers = int(sales_queried["Customer ID"].count())
        display_kpi("Total Customers", "{:,}".format(total_customers))

    with KPI_5:
        total_customers = int(sales_queried["Customer ID"].count())
        months_number = len(sales_queried["Month_Year"].unique())
        average_customers_per_month = round(divide(total_customers, months_number),2)
        display_kpi("Customers per Month", "{:,}".format(average_customers_per_month))

    category_column, subcategory_column = st.columns(2)

    sales_category = sales_queried.groupby(by=["Category"]).sum()[["Sales"]].sort_values(by=["Sales"])

    with category_column:
        category_horizontal_barchart = plot_bar_chart(sales_category,
                                                                "Sales",
                                                                sales_category.index,
                                                                "<b> Sales by Category</b>",
                                                                "h")
        st.plotly_chart(category_horizontal_barchart)

    sales_subcategory = sales_queried.groupby(by=["Subcategory"]).sum()[["Sales"]].sort_values(by=["Sales"])

    with subcategory_column:
        subcategory_horizontal_barchart = plot_bar_chart(sales_subcategory,
                                                                "Sales",
                                                                sales_subcategory.index,
                                                                "<b> Sales by Subcategory</b>",
                                                                 "h")
        st.plotly_chart(subcategory_horizontal_barchart)



    with st.container():
        line_chart = plot_line_chart(sales_queried, "Month_Year", "Sales", "<b>Sales by Month($)<b>")
        st.plotly_chart(line_chart, use_container_width=True)


    with st.container():
        map_lat = sales_queried.latitude
        map_long = sales_queried.longitude
        map_color = sales_queried.Region
        sales_queried = sales_queried.set_index('Sales')

        map = display_usa_map(sales_queried, "<b>Sales per State($)</b>", map_lat, map_long, map_color, sales_queried.index)
        st.plotly_chart(map, use_container_width=True)


    st.markdown(
        """
        <style>
        .css-1idizjf, .css-zi8otl, .css-16i25t9, .css-18ut3yg, .css-j5r0tf, .css-1r6slb0{
            border: 1px solid;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )