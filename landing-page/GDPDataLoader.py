import requests
import pandas as pd

def get_g10_gdp_change(year_start=2023, year_end=2024):
    
    g10_codes = ['BE', 'CA', 'FR', 'DE', 'IT', 'JP', 'NL', 'SE', 'CH', 'GB', 'US']

    all_data = []
    for code in g10_codes:
        url = f"https://api.worldbank.org/v2/country/{code}/indicator/NY.GDP.MKTP.CD"
        params = {
            "format": "json",
            "date": f"{year_start}:{year_end}",
            "per_page": 100
        }
        response = requests.get(url, params=params)
        data = response.json()

        if len(data) < 2:
            continue

        records = data[1]
        for record in records:
            country = record["country"]["value"]
            year = int(record["date"])
            value = record["value"]
            if value is not None:
                all_data.append({
                    "Country": country,
                    "Year": year,
                    "GDP (Current US$)": value
                })

    df = pd.DataFrame(all_data)

    # Pivot to have years as columns
    pivot_df = df.pivot(index="Country", columns="Year", values="GDP (Current US$)")

    # Drop countries with missing data
    pivot_df = pivot_df.dropna()

    # Calculate change and percent change
    pivot_df["GDP Change (US$)"] = pivot_df[year_end] - pivot_df[year_start]
    pivot_df["% Change"] = (pivot_df["GDP Change (US$)"] / pivot_df[year_start]) * 100

    # Convert to trillions and round
    pivot_df["GDP Start (Trillions)"] = pivot_df[year_start] / 1e12
    pivot_df["GDP End (Trillions)"] = pivot_df[year_end] / 1e12
    pivot_df["GDP Change (Trillions)"] = pivot_df["GDP Change (US$)"] / 1e12

    pivot_df = pivot_df.round({
        "GDP Start (Trillions)": 2,
        "GDP End (Trillions)": 2,
        "GDP Change (Trillions)": 2,
        "% Change": 2
    })

    # Sort by absolute GDP change descending
    result_df = pivot_df.sort_values(by="GDP Change (US$)", ascending=False)[[
        "GDP Start (Trillions)",
        "GDP End (Trillions)",
        "GDP Change (Trillions)",
        "% Change"
    ]]

    return result_df
