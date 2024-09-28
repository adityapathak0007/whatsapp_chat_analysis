from urlextract import URLExtract
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import pandas as pd
from collections import Counter
import emoji

# Ensure stopwords are downloaded only once
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #fetch the number of messages
    num_messages = df.shape[0]
    #fetch the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch the number of media messages
    num_media_messages = df[df['message'].str.contains('<Media omitted>', na=False)].shape[0]

    #fetch number of links shared
    # Initialize the links list before the loop
    links = []

    # Loop through each message in the 'message' column and extract URLs
    for message in df['message']:
        # Pass the message to the find_urls method
        found_links = extract.find_urls(message)
        links.extend(found_links)

    # Count the number of links found
    num_links = len(links)

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    # Get the top 5 users by message count
    x = df['user'].value_counts().head()

    # Calculate the percentage of messages sent by each user
    user_percentage = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    user_percentage.columns = ['name', 'percent']  # Renaming the columns

    return x, user_percentage


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Normalize message content: lowercase and strip whitespace
    df['message'] = df['message'].str.lower().str.strip()

    # Remove group notifications and omitted media messages
    temp = df[df['user'] != 'group_notification']

    # Filter out media omitted messages (case-insensitive and stripping whitespace)
    temp = temp[~temp['message'].str.contains('<media omitted>', case=False)]

    words = []
    # Loop through each message to collect words
    for message in temp['message']:
        for word in message.split():
            if word not in stop_words:  # Exclude stopwords
                words.append(word)

    # Set the font path to a Devanagari-compatible font (replace with the correct path)
    font_path = 'Nirmala.ttf'  # Example for Windows with 'Nirmala UI' font

    # Create a word cloud object
    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white',
        font_path=font_path  # Use the specified font
    )

    # Generate the word cloud
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Normalize message content: lowercase and strip whitespace
    df['message'] = df['message'].str.lower().str.strip()

    # Remove group notifications and omitted media messages
    temp = df[df['user'] != 'group_notification']

    # Filter out media omitted messages (case-insensitive and stripping whitespace)
    temp = temp[~temp['message'].str.contains('<media omitted>', case=False)]

    words = []
    # Loop through each message to collect words
    for message in temp['message']:
        for word in message.split():
            if word not in stop_words:  # Exclude stopwords
                words.append(word)

    # Create a DataFrame of the most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
    return most_common_df

def emoji_helper(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range (timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    # Filter the DataFrame for the selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap





