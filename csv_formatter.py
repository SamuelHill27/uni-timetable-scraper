import pandas as pd
import datetime

# convert days of the week to numbers where they will be incremented on to start week
def set_date(old_date, new_date, monday_date):
    new_date = monday_date
    days = old_date.replace(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], [0, 1, 2, 3, 4])

    # shift the start week date by the number associated with the day of the week above
    new_date += pd.to_timedelta(days, unit='D')

    new_date = new_date.dt.strftime('%d/%m/%Y')
    return new_date
    
# convert start time to 12 hour format with AM, PM appended on the end
def set_time(old_time, new_time):
    new_time = pd.to_datetime(old_time, format='%H:%M')
    new_time = new_time.dt.strftime('%I:%M %p')
    return new_time

# move data from original df to new df
def format_df(df, start_week):
    university = 'University of Nottingham'

    new_df = pd.read_csv('calendar_template.csv')

    # choose, from two appropriate columns, the one with the fewest nan's
    if df['Module Title'].isna().sum() <= df['Session Title'].isna().sum():
        new_df['Subject'] = df['Module Title']
    else:
        new_df['Subject'] = df['Session Title']

    new_df['Subject'].fillna(df['Type'], inplace=True)

    new_df['Start Date'] = set_date(df['Day'], new_df['Start Date'], start_week)
    new_df['Start Time'] = set_time(df['Start'], new_df['Start Time'])
    new_df['End Date'] = set_date(df['Day'], new_df['End Date'], start_week)
    new_df['End Time'] = set_time(df['End'], new_df['End Time'])

    new_df['All Day Event'] = 'FALSE'
    new_df['Description'] = df['Type'] + ' ' + df['Activity']

    new_df['Location'] = university + ' ' + df['Location']
    new_df['Location'].fillna(university, inplace=True)

    new_df['Private'] = 'TRUE'

    return new_df

def shift_week(dates):
    dates = pd.to_datetime(dates, format='%d/%m/%Y')
    dates += pd.to_timedelta(7, unit='D')
    dates = dates.dt.strftime('%d/%m/%Y')
    return dates

def repeat_df(df, repeat_num):
    shifted_df = df.copy()

    for _ in range(repeat_num):
        shifted_df['Start Date'] = shift_week(shifted_df['Start Date'])
        shifted_df['End Date'] = shift_week(shifted_df['End Date'])
        df = pd.concat([df, shifted_df], ignore_index=True)

    return df

def main():
    df = pd.read_csv('timetable.csv')

    start_week = datetime.datetime(2023, 9, 18)
    formatted_df = format_df(df, start_week)

    number_of_weeks = 10
    long_formatted_df = repeat_df(formatted_df, number_of_weeks)

    file = long_formatted_df.to_csv('formatted_timetable.csv')

    print('Formatting complete! ' + str(len(long_formatted_df)) + ' rows successfully formatted.')
    return file

if __name__ == '__main__':
    main()