import pandas as pd
import dbnomics as dn

DATA_POLLUTION = "AEA_16102022134617432.csv"
DATA_PRODUCTION = "SNA_TABLE31_16102022134511120.csv"
DATA_CURRENCIES = "DP_LIVE_16102022180940827.csv"

COLS = [
    'COUNTRY',
    'Country',
    'POLLUTANT',
    'Pollutant',
    'ACTIVITY_x',
    'Activity',
    'Measure_x',
    'MEASURE_x',
    'Year',
    'Unit Code_x',
    'Unit_x',
    'Value_x',
    'TRANSACT',
    'Transaction',
    'ACTIVITY_y',
    'Unit Code_y',
    'Unit_y',
    'Value_y'
]

GROUP_COLS = [
    'COUNTRY',
    'POLLUTANT',
    'ACTIVITY_x',
    'ACTIVITY_y',
    'Activity',
    'Unit_x',
    'Unit_y',
    'Unit Code_y'
]

MERGE_COLS = [
    'COUNTRY',
    'POLLUTANT',
    'ACTIVITY_x',
    'ACTIVITY_y',
    'Activity',
    'Unit_x',
    'Unit_y',
    'Unit Code_y',
    'Year'
]

MAIN_COLS = [
    'COUNTRY',
    'Country',
    'POLLUTANT',
    'ACTIVITY_x',
    'ACTIVITY_y',
    'Activity',
    'Unit_x',
    'Unit_y',
    'Unit Code_y',
    'Value_x',
    'Value_y',
    'Year'
]

CARBON_PRICE_PER_EUR = 75

pd.set_option('display.max_columns', None)

df_production = pd.read_csv(DATA_PRODUCTION)
df_pollution = pd.read_csv(DATA_POLLUTION)
df_fx = pd.read_csv(DATA_CURRENCIES)
df_fx = df_fx[(df_fx["INDICATOR"]=="EXCH") & (df_fx["SUBJECT"]=="TOT") & (df_fx["FREQUENCY"]=="A") & (df_fx["Flag Codes"].isna()==True)]

df_main = pd.merge(df_pollution, df_production, left_on=['Country','Year', 'Activity '], right_on = ['Country','Year', 'Activity'])

df_main = df_main[df_main['POLLUTANT'] == "GHG"]
df_main = df_main[df_main['TRANSACT'] == "SP1"]
df_main = df_main[df_main['Flag Codes_x'].isna() == True]
df_main = df_main[df_main['Flag Codes_y'].isna() == True]
df_main = df_main[df_main['MEASURE_y'] == "C"]

#df_main = df_main[['Year'] != 2020]
df_main = df_main[MAIN_COLS]
df_final = df_main.sort_values(by=MAIN_COLS)

""" 
dfs = [df_selector, df_main]
for d in dfs:
    print(d)
"""
df_final = df_final.merge(df_fx, how = "inner", left_on = ['COUNTRY', 'Year'], right_on = ['LOCATION', 'TIME'])
df_final.columns = [
    'ISO3',
    'COUNTRY',
    'POLLUTANT',
    'INDUSTRY CODE',
    'INDUSTRY CODE ALT',
    'INDUSTRY CODE DESC',
    'UNIT POLLUTANT',
    'CCY DESC',
    'CCY',
    'VALUE GHG',
    'VALUE OUTPUT',
    'YEAR',
    'LOCATION',
    'CCY INDICATOR',
    'SUBJECT',
    'MEASURE',
    'FREQUENCY',
    'TIME',
    'VALUE CCY',
    'FLAG CODE',
]
#Calculate the carbon intensity of the output, in pct
df_final['VALUE OUTPUT'] = df_final['VALUE OUTPUT'] * (10**6)
df_final = df_final[df_final['VALUE OUTPUT'] != 0]
df_final['CO2 LOAD'] = (df_final['VALUE GHG'] * CARBON_PRICE_PER_EUR / (df_final['VALUE OUTPUT']/df_final['VALUE CCY']))
df_final['ANNUAL REVENUE DEDUCTION FACTOR'] = df_final['CO2 LOAD'] * 0.1
df_final.to_csv("data.csv")

print(df_final)
print(df_final.describe())