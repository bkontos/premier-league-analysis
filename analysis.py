import pandas as pd

df = pd.read_csv('data/2021-2022.csv')

print(df)
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
