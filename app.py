import streamlit as st
import preprocessor,helper
import seaborn as sns
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")

import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    st.title("Top Statistics")

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages,num_of_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_of_links)
        # Monthly_timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily_timeline
        st.title("Daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time_day'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="yellow")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color ="red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # Activity Heatmap
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.figure(figsize=(20, 6))
        plt.yticks(rotation="horizontal")
        st.pyplot(fig)

        # Finding the busiest users in the group (group level)
        if selected_user =='Overall':
            st.title('Most busy user')
            x,new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                st.header("Bar graph")
                ax.bar(x.index, x.values,color='red')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title('Word Cloud')
        df_wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #common words
        st.title('Most frequent words')
        df_wc = helper.frequent_words(selected_user,df)
        # st.dataframe(df_wc)
        fig, ax = plt.subplots()
        ax.barh(df_wc[0], df_wc[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # emoji analysis
        st.title('Emoji analysis')
        emoji_df = helper.emoji_helper(selected_user,df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1],labels = emoji_df[0],autopct = "%0.2f")
            st.pyplot(fig)








