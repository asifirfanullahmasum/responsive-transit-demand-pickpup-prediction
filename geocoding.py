import os
from dotenv import load_dotenv
from geopy.geocoders import GoogleV3
import googlemaps
import pandas as pd
pd.set_option('expand_frame_repr', False)

load_dotenv()
api_key = os.getenv("API_KEY")

geolocator = GoogleV3(api_key)
gmaps = googlemaps.Client(key=api_key)

def load_data(path):
    data =  pd.read_csv(path)
    return data

def fetch_address(df, column_name):
    addresses = df[column_name]
    address_set = set(addresses)
    return address_set

def get_geocodes(addresses):
    addr_ext = ', Kalamazoo, Michigan, USA'
    address_dict = {}
    i = 1 
    for address in addresses:
        
        formatted_address = address + addr_ext
        location = geolocator.geocode(formatted_address)
        zip_code = None
        place_details = {}

        if location is not None:
            for component in location.raw['address_components']:
                if 'postal_code' in component['types']:
                    zip_code = component['long_name']
                    break
            place_id = location.raw['place_id']
            place_details = gmaps.place(place_id, fields=['name', 'type'])

            if 'result' in place_details:
                place_details = place_details['result']
            else:
                print("Failed to retrieve place details.")
        else:
            print("Geocoding failed. Please check the address and try again.")
        address_dict[address] = (location.latitude,location.longitude, zip_code, place_details.get('types', ['NA']))
        print(i, ' location geocoded', zip_code)
        i += 1
    return address_dict

def mapGeocodesToPickupAddress(geocodes, df):
    for key,value in geocodes.items():
        df.loc[(df['PickUp Address'] == key), ['PickUp Lat', 'PickUp Lng', 'PickUp Zipcode']] = [value[0],value[1], value[2]]
    return df

def mapGeocodesToDropoffAddress(geocodes, df):
    for key,value in geocodes.items():
        df.loc[(df['D/Off Address'] == key), ['D/Off Lat', 'D/Off Lng', 'D/Off Zipcode', 'D/Off Type']] = [value[0],value[1], value[2], value[3][0]]
    return df

# rdt_data = load_data('Metro Connect Trips October 2019_Cleaned.csv')
# pickups = fetch_address(rdt_data, 'PickUp Address')
# dropoffs = fetch_address(rdt_data, 'D/Off Address')
# pickups_geocodes = get_geocodes(pickups)
# dropoffs_geocodes = get_geocodes(dropoffs)
# rdt_geocode_data = mapGeocodesToPickupAddress(pickups_geocodes, rdt_data)
# rdt_geocode_data = mapGeocodesToDropoffAddress(dropoffs_geocodes, rdt_data)
# rdt_geocode_data.to_csv('Metro Connect Trips October 2019_Geocode.csv', index=False)