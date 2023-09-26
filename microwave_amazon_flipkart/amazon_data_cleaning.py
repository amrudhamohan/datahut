import pandas as pd
import re
import os

df = pd.read_csv('amazon_data_last3.csv')
df = df.replace({'‎': '', '%': '', '₹': ''}, regex=True)

# Drop rows with null values in the "brand" columns
df = df.dropna(subset=['Brand'])

# Replace "null" in "MRP Price" with "0"
df['MRP Price'] = df['MRP Price'].replace('null', 0)

# Fill blank number cells with '0'
df[['Product Price', 'MRP Price', 'Discount Percentage', 'Capacity']] = df[['Product Price', 'MRP Price', 'Discount Percentage', 'Capacity']].fillna(0)

# Fill null values with "null"
df = df.fillna('null')  

# Remove hyphen '-' from values in the "Discount Percentage" column
df['Discount Percentage'] = df['Discount Percentage'].str.replace('-', '')

# Extract only the numeric part from the "Capacity" column
df['Capacity'] = df['Capacity'].str.extract(r'(\d+)').astype(float)

# Remove rows where ASIN is null
df = df.dropna(subset=['ASIN'])

# Extract "Rating" and "Rating Count" from "Customer Reviews" column
df['Rating'] = df['Customer Reviews'].str.extract(r'^([\d.]+)')
df['Rating Count'] = df['Customer Reviews'].str.extract(r'([\d,]+)\s+ratings')

# Remove commas from "Rating Count" column
df['Rating Count'] = df['Rating Count'].str.replace(',', '')

# Convert "Rating Count" to numeric format
df['Rating Count'] = pd.to_numeric(df['Rating Count'], errors='coerce')

# Convert "Product Price" column to float
df['Product Price'] = df['Product Price'].str.replace(',', '').astype(float)

# Convert columns to integer format
df['MRP Price'] = df['MRP Price'].str.replace(',', '').astype(float)
df['Discount Percentage'] = df['Discount Percentage'].astype(float)

# Save the modified DataFrame back to the original CSV file
if os.path.exists('amazon_modified_file.csv'):
    os.remove('amazon_modified_file.csv')

df.to_csv('amazon_modified_file.csv', index=False)