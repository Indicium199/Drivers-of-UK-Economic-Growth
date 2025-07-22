# This is the script that takes data from the BIS API and cleanses it and transforms it for use in the dashboard

import requests
import zipfile
import io
import pandas as pd

# 1. Direct link for CBPOL flat CSV (from BIS bulk downloads)
zip_url = "https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip"

# 2. Download the ZIP
resp = requests.get(zip_url)
resp.raise_for_status()

# 3. Unzip and read the CSV
with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
    # Assume there's only one CSV in the ZIP
    csv_name = [name for name in z.namelist() if name.endswith(".csv")][0]
    df = pd.read_csv(z.open(csv_name), low_memory=False)

# Clean up column names: keep what's after the colon, or the original if no colon
df.columns = [col.split(":", 1)[-1].strip() for col in df.columns]

import pandas as pd

# Assuming your data is already loaded into a DataFrame called df

# Convert the date column to datetime
df['Time period or range'] = pd.to_datetime(df['Time period or range'], errors='coerce')

# Drop rows with missing values in relevant columns
df_clean = df.dropna(subset=['Time period or range', 'Observation Value'])

# Filter for the countries of interest
target_countries = ['GB: United Kingdom', 'US: United States', 'XM: Euro area', 'JP: Japan']
df_filtered = df_clean[df_clean['Reference area'].isin(target_countries)]

# Sort by date and get the latest record for each country
latest_rates = (
    df_filtered.sort_values(by='Time period or range')
    .groupby('Reference area', as_index=False)
    .last()[['Reference area', 'Time period or range', 'Observation Value']]
)

# Rename columns for clarity
latest_rates.columns = ['Country', 'Date', 'Interest Rate']

# Show the result
print(latest_rates)