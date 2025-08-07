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
