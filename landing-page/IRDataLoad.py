# Import libraries
import pandas as pd # For data manipulation
import requests # For making HTTP requests
import zipfile # For handling zip files
import io # For handling byte streams

def get_latest_rates():
    # Define the URL for the ZIP file for interest rate data from Bank of International Settlements
    url = "https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip"
    # Send a GET request to the URL
    response = requests.get(url)
    # Produce an error if the request was unsuccessful
    response.raise_for_status()

    # Open the ZIP file from the GET response
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Find the first CSV file from the ZIP file
        csv_name = [name for name in z.namelist() if name.endswith(".csv")][0]
        # Open and read the CSV file
        with z.open(csv_name) as f:
            # Decode the file content into a string, with error handling for decoding issues
            content = f.read().decode('utf-8', errors='replace')
            # Load the CSV content into a dataframe
            df = pd.read_csv(io.StringIO(content), low_memory=False)

    # Rename columns to make user friendly
    df.rename(columns={
        "REF_AREA:Reference area": "Country",
        "TIME_PERIOD:Time period or range": "Date",
        "OBS_VALUE:Observation Value": "Interest Rate"
    }, inplace=True)

    # Data cleanse and filter for latest date per country
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce") # Convert the Date column to datetime format, any invalid dates result in Not a Time
    df = df.dropna(subset=["Date", "Interest Rate"]) # Drop rows where Date or Interest rate is missing
    df.sort_values("Date", ascending=False, inplace=True) # Sort dataframe by date in descending order
    df = df[df["Country"].isin(["GB: United Kingdom", "US: United States", "JP: Japan", "XE: Euro area"])] # Filter dataframe for the countries GB, UK, JP and Euro Zone
    df = df.groupby("Country").first().reset_index() # Group data by country and select the latest record for each group

    # Create a dictionary to map country codes and names to the correct flag emoji
    country_flags = {
        "GB: United Kingdom": "🇬🇧",
        "US: United States": "🇺🇸",
        "JP: Japan": "🇯🇵",
        "XE: Euro area": "🇪🇺"
    }
    # Add a Flag column to the dataframe by mapping each country to its flag
    df["Flag"] = df["Country"].map(country_flags)

    # Clean country display names by removing country code and colon
    df["Country"] = df["Country"].str.replace(r'^[A-Z]{2}:\s*', '', regex=True)

    return df



