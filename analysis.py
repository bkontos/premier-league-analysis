import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as stats

df = pd.read_csv('data/2021-2022.csv')

# Convert 'Time' to datetime and create time bins
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time 
df['TimeBin'] = pd.cut(df['Time'].apply(lambda x:x.hour), bins=[0,12,17,24], labels=['Morning', 'Afternoon', 'Evening'])

# Function to determine win/loss/draw for home and away teams
def get_result(row):
    if row['FTHG'] > row['FTAG']:
        return ('Win', 'Loss')
    elif row['FTHG'] < row['FTAG']:
        return ('Loss', 'Win')
    else:
        return ('Draw', 'Draw')

# Apply the function to each row
df[['HomeResult', 'AwayResult']] = df.apply(get_result, axis=1, result_type='expand')

# Count wins, losses, and draws for each team based on time of day for home and away games
home_results = df.groupby(['HomeTeam', 'TimeBin'])['HomeResult'].value_counts().unstack().fillna(0)
away_results = df.groupby(['AwayTeam', 'TimeBin'])['AwayResult'].value_counts().unstack().fillna(0)

# Rename columns for clarity
home_results.columns = ['Home' + col for col in home_results.columns]
away_results.columns = ['Away' + col for col in away_results.columns]

# Combine home and away results
combined_results = home_results.join(away_results, how='outer', on=['HomeTeam', 'TimeBin']).fillna(0)

# Example: Print Liverpool's results
print("Liverpool's Results Based on Time of Day:")
print(combined_results.loc['Liverpool'])

# print(df)
''' Uncomment if you want to see if there is missing data
# Filter rows with at least one missing value
rows_with_missing_values = df[df.isnull().any(axis=1)]

# Iterate through each row
for index, row in df.iterrows():
    # Find columns with missing values in this row
    missing_columns = row[row.isnull()].index.tolist()
    
    # If there are missing columns, print the row index and missing column names
    if missing_columns:
        print(f"Row {index} has missing data in columns: {missing_columns}")

rows_with_missing_values.to_csv('rows_with_missing_values.csv', index=False)
'''
