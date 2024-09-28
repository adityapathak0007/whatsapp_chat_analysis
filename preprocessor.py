import re
import pandas as pd
from datetime import datetime
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
from textblob import TextBlob
import io
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess(data):
    # Pattern to match date and time in the WhatsApp chat format
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[APM]*\s*'
    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    # List to store formatted dates
    formatted_dates = []

    # Loop through each date string and handle flexible date parsing
    for date_str in dates:
        cleaned_date_str = date_str.replace('\u202f', '').strip()

        try:
            # Try parsing with 2-digit year
            dt = datetime.strptime(cleaned_date_str, '%m/%d/%y, %I:%M%p')
        except ValueError:
            # Fall back to 4-digit year parsing if the above fails
            dt = datetime.strptime(cleaned_date_str, '%m/%d/%Y, %I:%M%p')

        formatted_datetime = dt.strftime('%m/%d/%Y, %I:%M -')
        formatted_dates.append(formatted_datetime)

    # Create the DataFrame with messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': formatted_dates})

    # Convert 'message_date' to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%Y, %I:%M -')

    # Rename 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages using a more flexible pattern
    users = []
    messages = []

    for message in df['user_message']:
        # Match anything up to the first colon (user: message), allowing flexible usernames
        entry = re.split(r'^([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) > 1:
            users.append(entry[1].strip())  # Strip any extra spaces from the user name
            messages.append(entry[2].strip())  # Strip extra spaces from the message
        else:
            users.append('group_notification')
            messages.append(message.strip())  # Handle system messages

    # Add the 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract components from the 'date' column
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str(hour + 1))
        elif hour == 0:
            period.append(str('0') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
