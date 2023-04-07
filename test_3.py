import pandas as pd
from data_cleaning_v2 import standardizeDate
pd.set_option('expand_frame_repr', False)

DATA_DIR =  'Metro Connect Trips October 2019_Processed.csv'

def main():
    df =  pd.read_csv(DATA_DIR)
    df = df[1:].dropna()
    df = standardizeDate(df, 'Appt. Date', ['PickUp Time','Arrival Time'])
    df['Weekday'] = df['Appt. Date'].apply(lambda x: getWeekDay(x))
    df.to_csv('Metro Connect Trips October 2019_Processed.csv', index=False)

def getWeekDay(date):
    day_index = date.weekday()
    # Lookup the name of the day in a list
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_name = days[day_index]
    return day_name

if __name__ == '__main__':
    main()