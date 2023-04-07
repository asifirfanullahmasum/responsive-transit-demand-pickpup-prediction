import pandas as pd
from geocoding import fetch_address, get_geocodes, mapGeocodesToDropoffAddress, mapGeocodesToPickupAddress
pd.set_option('expand_frame_repr', False)

def preprocessData(path):
    df =  pd.read_csv(path)
    df = df[(df['Appt. Date'] !=  'Date') & (df['Acct'] !=  'Acct') & (df['Vehicle Code'] !=  'Code') & (df['Trip#'] !=  'Trip#') & (df['PickUp Time'] !=  'Time') & (df['PickUp Address'] !=  'Address') & (df['Arrival Time'] !=  'Time') & (df['D/Off Address'] !=  'Address') & (df['Rider Fare'] !=  'Fare')]
    df = df[1:].dropna()
    if ('PickUp Lat' not in df.columns) | ('PickUp Lng' not in df.columns) :
        print('Geocodes not available for Pickup Locations. Geocoding in progress :')
        df = geoCodePickup(df)
    if ('D/Off Lat' not in df.columns) | ('D/Off Lng' not in df.columns) :
        print('Geocodes not available for D/Off Locations. Geocoding in progress :')
        df = geoCodeDropoff(df)
    return df

def geoCodePickup(df):
    pickups = fetch_address(df, 'PickUp Address')
    pickups_geocodes = get_geocodes(pickups)
    geocoded_df = mapGeocodesToPickupAddress(pickups_geocodes, df)
    return geocoded_df

def geoCodeDropoff(df):
    dropoffs = fetch_address(df, 'D/Off Address')
    dropoffs_geocodes = get_geocodes(dropoffs)
    geocoded_df = mapGeocodesToDropoffAddress(dropoffs_geocodes, df)
    return geocoded_df


