import pandas as pd
import datetime
 
# # Creating a dataframe that stores records of students taking admission in a college
# data = pd.DataFrame({'AdmissionDate': ['2021-01-25','2021-01-22','2021-01-20',
#                         '2021-01-18','2021-01-22','2021-01-17','2021-01-21'],
#                      'StudentID': [7,5,3,2,6,1,4],
#                      'Name': ['Ram','Shyam','Mohan','Sohan','Lucky','Abhinav','Danny'],
#                      'Stream':['CSE','ECE','Civil','Mechanical','CSE','IT','EEE']
#                    })
# Checking dataframe
# print(data)

# # checking datatype
# print(type(data.AdmissionDate[0]))
 
# # convert to date
# data['AdmissionDate'] = pd.to_datetime(data['AdmissionDate'])
 
# # verify datatype
# print(type(data.AdmissionDate[0]))

# data = data.sort_values(by='AdmissionDate',ascending=False)
# print(data)


slots = {
"Slot 1" : (datetime.time(hour=12, minute=0),datetime.time(hour=15, minute=0)),
"Slot 2" : (datetime.time(hour=15, minute=0),datetime.time(hour=18, minute=0)),
"Slot 3" : (datetime.time(hour=21, minute=0),datetime.time(hour=23, minute=59)),
"Slot 4" : (datetime.time(hour=0, minute=0),datetime.time(hour=3, minute=0)),
"Slot 5" : (datetime.time(hour=3, minute=0),datetime.time(hour=6, minute=0)),
"Slot 6" : (datetime.time(hour=6, minute=0),datetime.time(hour=9, minute=0)),
"Slot 7" : (datetime.time(hour=9, minute=0),datetime.time(hour=12, minute=0))
}

# df = pd.DataFrame({
#     'timestamp': ['12:30:00', '12:10:00','15:45:00', '9:15:00']
# })

# df['timestamp'] = pd.to_datetime(df['timestamp']).dt.time

# slot_input = 'Slot 1'
# # Iterate over each row in the DataFrame
# final = df[(df['timestamp'] >= slots[slot_input][0]) & (df['timestamp'] < slots[slot_input][1])]
# print(final)

# def filterBySlot(df, time_column, slot_value):
#     df_filter = df[(df[time_column] >= slots[slot_value][0]) & (df[time_column] < slots[slot_value][1])]
#     return df_filter
# # print(slots)
# slot_list = list(slots.keys())
# slot_list.insert(0,'All')
# print(slot_list)


def getHoursMinsToAdd(initial_hour, initial_min, slot_length):
    # print('Intial :', initial_hour, initial_min)
    final_minutes = int((initial_min + slot_length) % 60)
    final_hour = int(initial_hour + int((initial_min + slot_length) / 60)) % 24
    # print('Final :', final_hour, final_minutes)
    return final_hour, final_minutes

def createSlots(slot_length = 60, starting_hour = 9, starting_min = 0):
    hour = starting_hour
    min = starting_min 
    time_slots = {}
    for i in range(1,int(24*60/slot_length)+1):    
        next_hour, next_min = getHoursMinsToAdd(hour,min,slot_length) 
        if next_min == 0:
            if next_hour == 0:
                # print(f"Slot {i} : {hour:d}:{min:02d} - {next_hour+23:d}:{next_min+59:02d}")
                time_slots[f"Slot {i} : {hour:d}:{min:02d} - {next_hour-1:d}:{next_min+59:02d}"] = (datetime.time(hour=hour, minute=min),datetime.time(hour=next_hour+23, minute=next_min+59))
            else:
                # print(f"Slot {i} : {hour:d}:{min:02d} - {next_hour-1:d}:{next_min+59:02d}")
                time_slots[f"Slot {i} : {hour:d}:{min:02d} - {next_hour-1:d}:{next_min+59:02d}"] = (datetime.time(hour=hour, minute=min),datetime.time(hour=next_hour-1, minute=next_min+59))
        else:
            # print(f"Slot {i} : {hour:d}:{min:02d} - {next_hour:d}:{next_min-1:02d}")
            time_slots[f"Slot {i} : {hour:d}:{min:02d} - {next_hour:d}:{next_min-1:02d}"] = (datetime.time(hour=hour, minute=min),datetime.time(hour=next_hour, minute=next_min-1))
        hour = next_hour
        min = next_min
        i += 1
    return time_slots

createSlots(30)
