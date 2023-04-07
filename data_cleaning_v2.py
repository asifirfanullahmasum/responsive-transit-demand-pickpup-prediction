import datetime
from data_cleaning_v1 import preprocessData
import pandas as pd
pd.set_option('expand_frame_repr', False)

DATA_DIR =  'Metro Connect Trips October 2019.csv'

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

def standardizeDate(df, date_column = None, time_columns = []):
    if date_column:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.date
    for column in time_columns:
        df[column] = pd.to_datetime(df[column], errors='coerce').dt.time
    return df

def sortByColumns(df, column = []):
    df = df.sort_values(by = column)
    return df

def filterByDays(df, date_column, date):
    df_filter = df[df[date_column] == pd.to_datetime(date).date()] 
    return df_filter

def mapTimeSlots(df, time_column, time_slots):
    for slot_keys, slot_value in time_slots.items():
        df.loc[(df[time_column] >= slot_value[0]) & (df[time_column] < slot_value[1]), 'Time Slots'] = slot_keys
    return df

def changeTo12Hours(df, time_column):
    df[time_column] = pd.to_datetime(df[time_column], format='%H:%M:%S').dt.strftime('%I:%M:%S %p')
    return df

def main():
    df = preprocessData(DATA_DIR)
    df = standardizeDate(df, 'Appt. Date', ['PickUp Time','Arrival Time'])
    df_sorted = sortByColumns(df,['Appt. Date'])
    df_final = mapTimeSlots(df_sorted, 'PickUp Time', createSlots())
    df_final.to_csv('Metro Connect Trips October 2019_Processed.csv', index=False)

if __name__ == "__main__":
    main()


