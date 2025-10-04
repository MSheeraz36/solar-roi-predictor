import requests
import pandas as pd

def get_solar_data(lat, lon, start_date, end_date):
    """
    Fetch solar irradiance from NASA POWER API
    Free, no authentication required!
    """
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    params = {
        'parameters': 'ALLSKY_SFC_SW_DWN',  # Solar irradiance
        'community': 'RE',  # Renewable Energy
        'longitude': lon,
        'latitude': lat,
        'start': start_date.replace('-', ''),
        'end': end_date.replace('-', ''),
        'format': 'JSON'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(
            data['properties']['parameter']['ALLSKY_SFC_SW_DWN'], 
            orient='index',
            columns=['solar_irradiance']
        )
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Test the function
if __name__ == "__main__":
    # Test with San Francisco coordinates
    print("Testing NASA API...")
    df = get_solar_data(37.7749, -122.4194, '2023-01-01', '2023-12-31')
    if df is not None:
        print("✅ API works!")
        print(f"Average solar irradiance: {df['solar_irradiance'].mean():.2f} kWh/m²/day")
        print(f"Data points collected: {len(df)}")
    else:
        print("❌ API failed")