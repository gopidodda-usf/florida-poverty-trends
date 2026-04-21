import pandas as pd
import requests

api_key = YOUR_API_KEY
years = list(range(2012,2025))
fl_fips_code = 12

all_data = {}
for year in years:
    url = f"https://api.census.gov/data/{year}/acs/acs5/subject?get=NAME,S1701_C03_001E&for=county:*&in=state:{fl_fips_code}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        columns = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows,columns = columns)
        
        df['Year'] = year
        all_data[year] = df

final_df = pd.concat(all_data.values())
final_df = final_df[['Year', 'NAME', 'S1701_C03_001E']]
final_df.columns = ['Year', 'County', 'Poverty Rate']
final_df['County'] = final_df['County'].astype(str).replace(' County, Florida', '')
final_df['Poverty Rate'] = pd.to_numeric(final_df['Poverty Rate'], errors = 'coerce')

pivot_df = final_df.pivot(index = 'Year', columns = 'County', values = 'Poverty Rate')
pivot_df.to_excel('florida_poverty_data_2012_2024.xlsx', sheet_name = 'County-Level Poverty Data')
