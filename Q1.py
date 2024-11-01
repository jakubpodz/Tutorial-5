"""Part 5 Tutorial Questions

The following are based on the Australian Tourism Dataset used in:

Hyndman, Rob J., Roman A. Ahmed, George Athanasopoulos, and Han Lin Shang. 2011. “Optimal Combination Forecasts for Hierarchical Time Series.” Computational Statistics & Data Analysis 55 (9): 2579–89..
Hollyman, Ross, Fotios Petropoulos, and Michael E. Tipping. 2021. “Understanding Forecast Reconciliation.” European Journal of Operational Research 294 (1): 149–60.

Amongst several others papers.

The data represent the number of overnight stays for domestic travel in Australia at monthly frequency.

1.	Open the dataset in excel and note carefully the format of the file
2.	Load the data into a Pandas DataFrame called 'oztour'
3.	Introduce a new date based index for the 'oztour' DataFrame:
    - This will require a few steps... it is good practice to work out what these are...
    (hint: check out the keyword arguments to the pd.Series.fillna(), then use pd.to_datetime)
    Convert the existing date information into a pandas period index (which represents the whole month rather than just a point in time)
    Set the dataframe index to take these values
4.	The column names indicate Geographic States, Zones and Regions of Australia (first three letters respectively)
    and the purpose of travel. Using the pd.groupby() command:
    a.	Report a DataFrame 'PoT' showing the data summed by purpose of travel, assign the resulting DataFrame
    b.	Report a DataFrame 'State' showing the data summed by state
    c.	Report a DataFrame 'PoT_State' showing summed by state and purpose of travel
5.	Report a DataFrame 'corr_mat' containing the correlation matrix of the data series summed by state and purpose of travel, rounded to 2 decimal places.
    (hint Pandas has commands for both steps)
6.	Report a DataFrame 'PoT_State_By_Year' containing the data summed by state and purpose of travel, as above,
    then further aggregated by Calendar Year.
7.	An alternative approach is to aggregate the data over time using the pd.resample() command.
    a.	Plot the monthly data summed by purpose of travel using df.plot() (more on this next week!)
    b.	Reseample the data to Quarterly and Yearly frequency using df.resample(‘Q’) and df.resample(‘Y’) commands. Plot both charts.
    c.	Which chart makes the trends (as opposed to the seasonality) in the data easier to see?"""

import pandas as pd
import numpy as np

oztour = pd.read_csv('TourismData_v3.csv')
oztour.head()

oztour['Year'] = oztour['Year'].fillna(method='ffill') #forwqard fill na values
oztour['Year'] = oztour['Year'].astype(int) 

#create a dictionary coinatining months and corresponding numerical key
month_to_num = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

#change the monthly column to to numeric where lambda applys the keys of dict
oztour['Month'] = oztour['Month'].apply(lambda x: month_to_num[x])

oztour['Date'] = pd.to_datetime(oztour['Year'].astype(str) + '-' + oztour['Month'].astype(str)) #combine month and year
oztour.set_index('Date', inplace=True)

oztour.drop(columns=['Year', 'Month'], inplace=True)

oztour.index = oztour.index.to_period('M')

#extract the first 3 letters for state and remining letters for pot
pot_mapping = {col: col[3:] for col in oztour.columns}
state_mapping = {col: col[:3] for col in oztour.columns}
grouped_pot = oztour.groupby(pot_mapping, axis=1).sum() 
grouped_state = oztour.groupby(state_mapping, axis=1).sum()

multi_level_mapping = {(col[:3], col[3:]): col for col in oztour.columns}
oztour.columns = pd.MultiIndex.from_tuples([(col[:3], col[3:]) for col in oztour.columns], names=['State', 'Purpose'])
PoT_State = oztour.groupby(level=['State', 'Purpose'], axis=1).sum()

corr_mat = PoT_State.corr()
corr_mat = corr_mat.round(2)

print(corr_mat)


PoT_State_By_Year = PoT_State.resample('Y').sum()


grouped_pot.plot(title="Monthly Data Summed by Purpose of Travel", figsize=(10, 6))

PoT_Quarterly = grouped_pot.resample('Q').sum()
PoT_Quarterly.plot(title="Quarterly Data Summed by Purpose of Travel", figsize=(10, 6))

PoT_Yearly = grouped_pot.resample('Y').sum()
PoT_Yearly.plot(title="Yearly Data Summed by Purpose of Travel", figsize=(10, 6))

##The graph that shows the most clarity is the resampled year plot as it smooths out short-term and seasonal fluctuations that helps show long-term movements.



