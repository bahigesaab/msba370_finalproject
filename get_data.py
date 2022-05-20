import streamlit as st
import pandas as pd
import numpy as np

@st.cache
def get_data_from_csv():
    sales = pd.read_csv('Sales_Data.csv', encoding='ISO-8859-1')
    # Add 'Month' and 'Year' from 'Order Date' column
    sales['Month'] = pd.to_datetime(sales['Order Date']).dt.month
    sales['Year'] = pd.to_datetime(sales['Order Date']).dt.year
    sales['Month_Year'] = pd.to_datetime(sales['Order Date']).dt.strftime('%m/%Y')
    new_columns = {"Order Date":"Order_Date", "Ship Date":"Ship_Date", "Customer Name": "Customer_Name",\
    "Sub-Category":"Subcategory", "Shipping Cost":"Shipping_Cost", "Product Name": "Product"}
    sales.rename(columns=new_columns, inplace=True)
    return sales


@st.cache
def get_usa_data_from_csv():
    sales = pd.read_csv('Sales_Data.csv', encoding='ISO-8859-1')
    us_sales = sales["Country"]=="United States"
    sales=sales[us_sales]
    wanted_regions = sales["Region"].isin(["North","South","East","West","Central"])
    sales=sales[wanted_regions]
    # Add 'Month' and 'Year' from 'Order Date' column
    sales['Month'] = pd.to_datetime(sales['Order Date']).dt.month
    sales['Year'] = pd.to_datetime(sales['Order Date']).dt.year
    sales['Month_Year'] = pd.to_datetime(sales['Order Date']).dt.strftime('%Y/%m')
    new_columns = {"Order Date":"Order_Date", "Ship Date":"Ship_Date", "Customer Name": "Customer_Name",\
    "Sub-Category":"Subcategory", "Shipping Cost":"Shipping_Cost", "Product Name": "Product"}
    sales.rename(columns=new_columns, inplace=True)
    return sales


@st.cache
def get_world_data_from_csv():
    sales = pd.read_csv('Sales_Data.csv', encoding='ISO-8859-1')
    world_sales = sales["Country"]!="United States"
    sales=sales[world_sales]
    # unwanted_regions = ~sales["Region"].isin(["North","South","East","West","Central"])
    # sales=sales[unwanted_regions]
    # Add 'Month' and 'Year' from 'Order Date' column
    sales['Order Date'] = pd.to_datetime(sales['Order Date'])
    sales['Month'] = pd.to_datetime(sales['Order Date']).dt.month
    sales['Year'] = pd.to_datetime(sales['Order Date']).dt.year
    sales['Month_Year'] = pd.to_datetime(sales['Order Date']).dt.strftime('%Y-%m')
    new_columns = {"Order Date":"Order_Date", "Ship Date":"Ship_Date", "Customer Name": "Customer_Name",\
    "Sub-Category":"Subcategory", "Shipping Cost":"Shipping_Cost", "Product Name": "Product"}
    sales.rename(columns=new_columns, inplace=True)
    return sales


def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        return None
    else:
        return result

# https://www.webfx.com/tools/emoji-cheat-sheet/world_sales_analytics.py