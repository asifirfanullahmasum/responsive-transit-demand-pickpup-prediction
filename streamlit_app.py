import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import st_folium
import pandas as pd

pd.set_option('expand_frame_repr', False)

APP_TITLE = 'RDT Data Analysis'
APP_HEADER_VISUALIZATION = 'RDT Data Analysis & Visualization'
APP_HEADER_PREDICTION = 'RDT Data Prediction'
APP_SUBHEADER = 'Source: K-Metro Transit Data'

st.set_page_config(layout="wide", page_title=APP_TITLE)

selected = option_menu(
    menu_title= None, 
    options= ["Data Analysis", "Data Prediction"], 
    icons= ['graph-up', 'lightbulb-fill'], 
    default_index= 0, 
    orientation= "horizontal",
    key=None
)

slot_size = {
    '15 Minutes': 15,
    '30 Minutes': 30,
    '1 Hour': 60,
    '2 Hours': 120,
    '3 Hours' : 180
}

def main():
    st.write(selected)
    df = readData('Metro Connect Trips October 2019_Geocoded.csv')
    if selected == 'Data Analysis':
        showVisualization(df)
    elif selected == 'Data Prediction':
        showPrediction(df)
    # st.empty()

def getHoursMinsToAdd(initial_hour, initial_min, slot_length):
    final_minutes = int((initial_min + slot_length) % 60)
    final_hour = int(initial_hour + int((initial_min + slot_length) / 60)) % 24
    return final_hour, final_minutes

def createSlots(slot_length = 60, starting_hour = 9, starting_min = 0):
    hour = starting_hour
    min = starting_min 
    time_slots = {}
    for i in range(1,int(24*60/slot_length)+1):    
        next_hour, next_min = getHoursMinsToAdd(hour,min,slot_length) 
        if next_min == 0:
            if next_hour == 0:
                time_slots[f"Slot {i} : {hour:d}:{min:02d} - {next_hour-1:d}:{next_min+59:02d}"] = (datetime.time(hour=hour, minute=min),datetime.time(hour=next_hour+23, minute=next_min+59))
            else:
                time_slots[f"Slot {i} : {hour:d}:{min:02d} - {next_hour-1:d}:{next_min+59:02d}"] = (datetime.time(hour=hour, minute=min),datetime.time(hour=next_hour-1, minute=next_min+59))
        else:
            time_slots[f"Slot {i} : {hour:d}:{min:02d} - {next_hour:d}:{next_min-1:02d}"] = (datetime.time(hour=hour, minute=min),datetime.time(hour=next_hour, minute=next_min-1))
        hour = next_hour
        min = next_min
        i += 1
    return time_slots

def showPrediction(df):
    st.title(APP_HEADER_PREDICTION)
    st.caption(APP_SUBHEADER)

    df_cleaned = standardizeDate(df, 'Appt. Date', 'PickUp Time')
    df_sortedby_date = sortByColumns(df_cleaned,['Appt. Date'])
    start_date, stop_date = getDateRange(df_sortedby_date, 'Appt. Date')
    time_slots = createSlots()

    acct_list = list(df_sortedby_date['Acct'].unique())
    acct_list.insert(0,'All')
    slots_list = list(time_slots.keys())
    slots_list.insert(0,'All')

    selected_date = st.sidebar.date_input('Select a date', start_date, min_value=start_date, max_value=stop_date)
    selected_slot = st.sidebar.selectbox('Select a Slot', slots_list)
    selected_acct = st.sidebar.selectbox('Select a Acct Type', acct_list)

    st.write('Under Construction')
    
def showVisualization(df):
    st.title(APP_HEADER_VISUALIZATION)
    st.caption(APP_SUBHEADER)

    df_cleaned = standardizeDate(df, 'Appt. Date', 'PickUp Time')
    df_sortedby_date = sortByColumns(df_cleaned,['Appt. Date'])
    start_date, stop_date = getDateRange(df_sortedby_date, 'Appt. Date')
    selected_date = st.sidebar.date_input('Select a date', start_date, min_value=start_date, max_value=stop_date)


    selected_slot_size = st.sidebar.selectbox('Select a Slot Size', list(slot_size.keys()), index = 2)
    time_slots = createSlots(slot_size[selected_slot_size])
    slots_list = list(time_slots.keys())
    slots_list.insert(0,'All')
    selected_slot = st.sidebar.selectbox('Select a Slot', slots_list)

    acct_list = list(df_sortedby_date['Acct'].unique())
    acct_list.insert(0,'All')
    selected_acct = st.sidebar.selectbox('Select a Acct Type', acct_list)
    
    st.write('Showing results for : | Date - ', selected_date, " | Slot - ", selected_slot, " | Acct - ", selected_acct)
    
    df_filtered =  filterByDays(df_sortedby_date, 'Appt. Date', selected_date)
    df_filtered = sortByColumns(df_filtered,['PickUp Time'])
    
    if selected_acct != 'All':
        df_filtered = filterByACCT(df_filtered, 'Acct', selected_acct)

    if selected_slot != 'All':
        df_filtered = filterBySlot(df_filtered, 'PickUp Time', time_slots, selected_slot)

    styled_df = df_filtered.reset_index(drop=True)

    centre_location = [42.291585, -85.587284] #Kalamazoo Geocode
    pickups = getPickupLocations(df_filtered)

    displayMap(centre_location, pickups)
    st.dataframe(styled_df, width=1600, height = 500)

def initializeMap(centre_location):
    map = folium.Map(location = centre_location, zoom_start=12)
    return map

def addMarker(map, locations, color):
    for location in locations:
        folium.Marker(location=location, icon=folium.Icon(color=color)).add_to(map)
    return map

def displayMap(centre_location, pickup = [], dropoff = []):

    map = initializeMap(centre_location)
    st.write("Map Visualization")

    # Add pickup Markers
    if len(pickup):
        addMarker(map, pickup, 'green')
    # Add dropoff Markers
    if len(dropoff):
        addMarker(map, dropoff, 'red')
    
    st_folium(map, width=1600, height=800)


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

def getDateRange(df, date_column):
    start_date = df[date_column].head(1)
    stop_date = df[date_column].tail(1)
    return start_date.values[0], stop_date.values[0]

def standardizeDate(df, date_column, time_column):
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.date
    df[time_column] = pd.to_datetime(df[time_column], errors='coerce').dt.time
    return df

def changeTo12Hours(df, time_column):
    df[time_column] = pd.to_datetime(df[time_column], format='%H:%M:%S').dt.strftime('%I:%M:%S %p')
    return df

def sortByColumns(df, column = []):
    df = df.sort_values(by = column)
    return df

def filterByDays(df, date_column, date):
    df_filter = df[df[date_column] == pd.to_datetime(date).date()] 
    return df_filter

def filterByACCT(df, acct_column, acct_value):
    df_filter = df[df[acct_column] == acct_value] 
    return df_filter

def filterBySlot(df, time_column, time_slots, slot_value):
    df_filter = df[(df[time_column] >= time_slots[slot_value][0]) & (df[time_column] < time_slots[slot_value][1])]
    return df_filter

def readData(path):
    df =  pd.read_csv(path)
    return df
    
if __name__ == "__main__":
    main()