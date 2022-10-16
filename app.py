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

st.header("Sources")
st.write(
    "**OECD Supply Tables**:" + r"https://stats.oecd.org/Index.aspx?DataSetCode=SNA_TABLE31"
)

with st.expander("Source description"):
    st.write("It presents the breakdown of output at basic prices between market output, \\\
        output for own final use and non-market output, by activty at the 2 digit ISIC Rev 4 level. \\\
        It has been prepared from statistics reported to the OECD by countries in their answers to \\\
        Supply and Use questionnaire.")

st.write(
    "**OECD GHG Air Emissions**:" + r"https://stats.oecd.org/viewhtml.aspx?datasetcode=AEA&lang=en"
)

with st.expander("Source description"):
    st.write("Air Emission Accounts are available for European countries and a few non-European countries. \\\
        The System of Environmental-Economic Accounting (SEEA) Central Framework is an accounting system developed around two objectives: \\\
        'understanding the interactions between the economy and the environment' and describing \\\
        'stocks and changes in stocks of environmental assets'. The SEEA combines national accounts \\\
        and environmental statistics in a statistical framework with consistent definitions, classifications \\\
        and concepts allowing policy makers to evaluate environmental pressures from economic activities at macro- and meso-levels.")
    st.write("Data refer to total emissions of CO2 (CO2 emissions from energy use and industrial processes, e.g. \\\
        cement production), CH4 (methane emissions from solid waste, livestock, mining of hard coal and lignite, \\\
        rice paddies, agriculture and leaks from natural gas pipelines), N2O (nitrous oxide), HFCs (hydrofluorocarbons), \\\
        PFCs (perfluorocarbons), (SF6 +NF3) (sulphur hexafluoride and nitrogen trifluoride), SOx (sulphur oxides, NOx  \\\
        (nitrogen oxides), CO (carbon monoxide), NMVOC (non-methane volatile organic compounds), PM2.5 (particulates less \\\
        that 2.5 µm), PM10 (particulates less that 10 µm) and NH3 (ammonia).")
    st.write("The OECD Air Emission Accounts present data based on ISIC rev. 4.")