import pandas as pd
from data_cleaning_v2 import createSlots, standardizeDate
pd.set_option('expand_frame_repr', False)

DATA_DIR =  'Dummy Dataset for Visualization.csv'

def main():
    records = 1
    df =  pd.read_csv(DATA_DIR)
    df = df[1:].dropna()
    week = df['Weekday'].unique()
    acct = df['Acct'].unique()
    timeslot = list(createSlots(180).keys())
    zipcodes = df['PickUp Zipcode'].unique()

    for zips in zipcodes:
        for day in week:
            for slot in timeslot:
                for ac in acct: 
                    df.loc[records, ['PickUp Zipcode','Weekday', 'Time Slots', 'Acct',  ]] = [zips, day, slot, ac]
                    records += 1
    df = df[:records]
    print(df.head())
    df.to_csv('Dummy Dataset.csv', index=False)

if __name__ == '__main__':
    main()
