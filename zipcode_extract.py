import os
from dotenv import load_dotenv
import googlemaps
from geopy.geocoders import GoogleV3

load_dotenv()
api_key = os.getenv("API_KEY_ALT")

# Address to look up
address = '8850 Shaver Rd, Kalamazoo, MI'

# Create GoogleV3 geocoder instance
geolocator = GoogleV3(api_key)
gmaps = googlemaps.Client(key=api_key)

# Geocode address
#location = geolocator.geocode(address)

def main():
    # Extract ZIP code from location
    zip_code = None

    location = geolocator.geocode("1600 Amphitheatre Parkway, Mountain View, CA 94043, USA", exactly_one=True, timeout=10)

    if location is not None:
        for component in location.raw['address_components']:
            if 'postal_code' in component['types']:
                zip_code = component['long_name']
                break
        place_id = location.raw['place_id']
        place_details = gmaps.place(place_id, fields=['name', 'type'])

        if 'result' in place_details:
            print(place_details['result'])
        else:
            print("Failed to retrieve place details.")
    else:
        print("Geocoding failed. Please check the address and try again.")


if __name__ == '__main__':
    main()