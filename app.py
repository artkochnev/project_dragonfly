import streamlit as st
import pandas as pd
import plotly.express as px 

DATA = "data.csv"
RENDER_COLS = ["INDUSTRY CODE DESC", "ANNUAL REVENUE DEDUCTION FACTOR"]

# EXTRA FUNCTIONS
def convert_df(df):
   return df.to_csv(index = False).encode('utf-8')

# LOAD DATA
df_main = pd.read_csv(DATA)
country_list = df_main["COUNTRY"].unique()
year_list = df_main["YEAR"].unique()

# DASHBOARD
st.title("CLIMATE REVENUE DISCOUNT FACTORS")
st.write("Factors show the annual increase of company costs measured as percent of industry revenues driven by the carbon price increase. Calculated according to the formula below")
st.latex(r'''
    \delta = \frac{\text{CO2 Emissions(tn)} \times \text{ETS Price(USD/tn)}}{\text{Industry Output, USD}} \times \text{Tax rate}
    ''')
st.write("Tax rate assumed to be 10%, which is the carbon price increase compatible with the 1.5 degree goal")

st.header('Discount Factors per industry and country')
country_choice = "AUD"
country_choice = st.selectbox(
    'Select the country',
    country_list)
year_choice = 2019
year_choice = st.selectbox(
    'Select the year',
    year_list)

df_render = df_main[(df_main['COUNTRY'] == country_choice) & (df_main['YEAR'] == year_choice)]

# LOAD GRAPHS
fig=px.bar(df_render,y='INDUSTRY CODE DESC', x='ANNUAL REVENUE DEDUCTION FACTOR', orientation='h')
st.write(fig)

st.header("Download industry factors for the selected country")

csv = convert_df(df_render)
st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

st.header('Full dataset')
st.write(df_main)