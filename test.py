import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
from textblob import TextBlob
import io
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# App title and sidebar
st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp Chat File")

# Load and preprocess data
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    df['user'] = df['user'].str.strip()

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analyze Chat By", user_list)

    if st.sidebar.button("Show Analysis"):
        # Show top statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Chat Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", num_media_messages)
        col4.metric("Links Shared", num_links)

        # Monthly timeline with Plotly
        st.title("Monthly Activity")
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', title='Monthly Messages', markers=True)
        st.plotly_chart(fig)

        # Daily timeline
        st.title("Daily Activity")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig = px.line(daily_timeline, x='only_date', y='message', title='Daily Messages', markers=True)
        st.plotly_chart(fig)

        # Activity map: busiest day and month
        st.title("Activity Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Busiest Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig = plt.figure(figsize=(10, 5))
            sns.barplot(x=busy_day.index, y=busy_day.values, palette="viridis")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Busiest Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig = plt.figure(figsize=(10, 5))
            sns.barplot(x=busy_month.index, y=busy_month.values, palette="inferno")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heatmap for weekly activity
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(user_heatmap, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # Most busy users for group chat
        if selected_user == 'Overall':
            st.title("Most Active Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Message Count")
                fig = plt.figure(figsize=(10, 5))
                sns.barplot(x=x.index, y=x.values, palette="rocket")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.subheader("Detailed Stats")
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=most_common_df['Count'], y=most_common_df['Word'], palette='magma')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analysis with pie chart
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        # Emoji analysis with customizable pie chart (without emoji slider)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        # Display emoji DataFrame
        with col1:
            st.dataframe(emoji_df)

        # Automatically display the top emojis without using a sidebar slider
        with col2:
            # Filter the top emojis based on a predefined threshold (e.g., top 5 emojis)
            emoji_threshold = 5  # You can adjust this value to control how many emojis to show
            filtered_emoji_df = emoji_df[emoji_df[1] >= emoji_threshold]  # Filter emoji data based on this threshold

            # Check if the filtered emoji DataFrame is not empty
            if not filtered_emoji_df.empty:
                fig, ax = plt.subplots(figsize=(15, 15))  # Create a large pie chart

                wedges, texts, autotexts = ax.pie(
                    filtered_emoji_df[1].head(),  # Top emojis
                    labels=filtered_emoji_df[0].head(),
                    autopct="%.2f%%",
                    startangle=90,
                    textprops={'fontsize': 20},  # Customize percentage label size
                    colors=plt.get_cmap('tab20').colors  # Use a nice color palette
                )

                # Add a legend for better visualization
                ax.legend(wedges, filtered_emoji_df[0].head(), title="Top Emojis", loc="center left",
                          bbox_to_anchor=(1, 0, 0.5, 1))
                st.pyplot(fig)
            else:
                st.warning("No emojis found with the selected threshold.")


        # Sentiment analysis
        st.title("Sentiment Analysis")
        df['sentiment'] = df['message'].apply(lambda msg: TextBlob(msg).sentiment.polarity)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['sentiment'], bins=50, kde=True, color='green')
        plt.title("Sentiment Distribution")
        st.pyplot(fig)

        # Download chat data as CSV
        st.sidebar.title("Download Data")
        csv_data = df.to_csv().encode('utf-8')
        st.sidebar.download_button(label="Download CSV", data=csv_data, file_name="chat_data.csv", mime='text/csv')
