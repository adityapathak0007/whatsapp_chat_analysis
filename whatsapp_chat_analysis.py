import re
import pandas as pd
from datetime import datetime

# Read the WhatsApp chat data
f = open("D:\\Aditya's Notes\\All Projects\\Whats App Chat Analysis\\mkclgroup.txt", 'r', encoding='utf-8')
data = f.read()

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
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month_name()
df['day'] = df['date'].dt.day
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute

# Output the resulting DataFrame
print(df.head())
print(df.shape)
