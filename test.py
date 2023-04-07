import pandas as pd
from test_2 import createSlots
pd.set_option('expand_frame_repr', False)

DATA_DIR =  'Metro Connect Trips October 2019_Processed.csv'

def standardizeDate(df, time_columns = [], date_column = None):
    if date_column:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.date
    for column in time_columns:
        df[column] = pd.to_datetime(df[column], errors='coerce').dt.time
    return df

def mapTimeSlots(df, time_column, time_slots):
    df = standardizeDate(df, ['PickUp Time','Arrival Time'])
    for slot_keys, slot_value in time_slots.items():
        df.loc[(df[time_column] >= slot_value[0]) & (df[time_column] <= slot_value[1]), 'Time Slots'] = slot_keys
    return df

df =  pd.read_csv(DATA_DIR)

time_slots = createSlots()

final_df = mapTimeSlots(df, 'PickUp Time', time_slots)

final_df.to_csv('Metro Connect Trips October 2019_Processed.csv', index=False)


