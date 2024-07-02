import re
import pandas as pd
from datetime import datetime
import date_fix
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    pattern1 = re.compile(r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?[APMapm]{2})')
    messages = re.split(pattern, data)[1:]
    if len(messages) == 0:
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        pattern1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern1, data)
    else:
        dates = pattern1.findall(data)


#Upper want to fix for xtra features
    fmt=date_fix.format_find(dates)
    df = pd.DataFrame({'u_dms': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format=fmt)

    users = []
    messages = []

    for dm in df['u_dms']:
        entry = re.split('([\w\W]+?):\s', dm)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append("Notification")
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['u_dms'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['o_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for i in range(df.shape[0]):
        hour = df['hour'][i]
        if hour == 23:
            period.append(str(hour) + "-" + str(0))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df

