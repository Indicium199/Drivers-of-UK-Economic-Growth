# EmpRatesDataLoad.py

import pandas as pd
import requests
from io import StringIO

def get_latest_unemployment():
    url = "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Load CSV, skipping metadata rows
    data = StringIO(response.text)
    df = pd.read_csv(data, skiprows=8)

    # Rename columns
    df.columns = ['Date', 'Unemployment Rate']

    # Drop empty rows
    df = df.dropna(subset=['Date', 'Unemployment Rate'])

    # Parse date robustly
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')

    # Drop rows where date parsing failed
    df = df.dropna(subset=['Date'])

    # Add static country
    df['Country'] = 'United Kingdom'

    return df

def get_latest_awe():
    url = "https://www.ons.gov.uk/generator?uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/averageweeklyearningsingreatbritain/june2025/c7cd254e&format=csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = StringIO(response.text)
    df = pd.read_csv(data, skiprows=8)
    
    # Keep only first 2 columns (Month-Year, Value)
    df = df.iloc[:, [0, 1]]
    df.columns = ['Date', 'Average Weekly Earnings']
    
    # Convert 'Feb 2000' style text to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%b %Y', errors='coerce')
    
    # Drop rows where parsing failed
    df = df.dropna(subset=['Date', 'Average Weekly Earnings'])
    
    # Ensure numeric
    df['Average Weekly Earnings'] = pd.to_numeric(df['Average Weekly Earnings'], errors='coerce')
    df = df.dropna(subset=['Average Weekly Earnings'])
    
    df['Country'] = 'United Kingdom'
    return df


# Test
if __name__ == "__main__":
    df_awe = get_latest_awe()
    print(df_awe.head())