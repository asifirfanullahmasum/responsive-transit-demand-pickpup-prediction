import folium
from folium.plugins import MarkerCluster
from IPython.display import IFrame
import pandas as pd


def load_data(path):
    data =  pd.read_csv(path)
    return data

def initializeMap(centre_location):
    map = folium.Map(location = centre_location, zoom_start = 13)
    return map

def addMarker(map, locations, color):
    for location in locations:
        folium.Marker(location=location, icon=folium.Icon(color=color)).add_to(map)
    return map

def displayMap(centre_location, pickup = [], dropoff = []):

    map = initializeMap(centre_location)

    # Add pickup Markers
    if len(pickup):
        addMarker(map, pickup, 'green')
    # Add dropoff Markers
    if len(dropoff):
        addMarker(map, dropoff, 'red')
    #Display the map
    map.save('map.html')
    # Display the map using IFrame
    IFrame(src='./map.html', width=700, height=600)

def getPickupLocations(df):
    locations = []
    for index, row in df.iterrows():
        locations.append([row['PickUp Lat'],row['PickUp Lng']])
    return locations

def getDropoffLocations(df):
    locations = []
    for index, row in df.iterrows():
        locations.append([row['D/Off Lat'],row['D/Off Lng']])
    return locations

def main():
    rdt_data = load_data('Metro Connect Trips October 2019_Geocode.csv')
    pickups = getPickupLocations(rdt_data[0:5000])
    dropoffs = getDropoffLocations(rdt_data)   
    kzoo = [42.291585, -85.587284]
    displayMap(kzoo, pickups)

if __name__ == "__main__":
    main()





