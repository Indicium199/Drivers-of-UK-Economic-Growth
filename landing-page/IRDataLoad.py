def get_latest_rates():
    # Download and load the dataset as you already do
    import requests, zipfile, io
    import pandas as pd

    url = "https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip"
    resp = requests.get(url)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        csv_name = [name for name in z.namelist() if name.endswith(".csv")][0]
        df = pd.read_csv(z.open(csv_name), low_memory=False)

    # Rename for convenience
    df = df.rename(columns={
        'REF_AREA:Reference area': 'Country',
        'TIME_PERIOD:Time period or range': 'Date',
        'OBS_VALUE:Observation Value': 'Interest Rate'
    })

    # Parse date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date', 'Interest Rate'])

    # Extract 2-letter code
    df['Code'] = df['Country'].str.extract(r'^([A-Z0-9]{2})')

    # Filter desired countries
    target_codes = ['GB', 'US', 'JP', 'EZ', 'EA', 'U2']
    df = df[df['Code'].isin(target_codes)]

    # Drop duplicates: keep latest per country
    latest_df = df.sort_values('Date').drop_duplicates(subset='Code', keep='last')

    # Map flags
    flag_map = {
        'GB': '🇬🇧',
        'US': '🇺🇸',
        'JP': '🇯🇵',
        'EZ': '🇪🇺',
        'EA': '🇪🇺',
        'U2': '🇪🇺'
    }
    latest_df['Flag'] = latest_df['Code'].map(flag_map)

    return latest_df[['Country', 'Interest Rate', 'Flag']]
