from urlextract import URLExtract
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()
from wordcloud import WordCloud
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch number of messages
    num_messages = df.shape[0]
    # fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages,len(links)


def most_busy_users(df):

    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns ={'user':'name','count':'percent'})
    return x,df

def create_word_cloud(selected_user,df):
    h = open('hinglish.txt', 'r')
    stop_words = h.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch number of messages
    temp = df[df['message'] != "<Media omitted>\n"]
    temp = temp[temp['user'] != "group_notification"]

    def remove_stop_words(message):
        y =[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    # fetch number of messages
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def frequent_words(selected_user,df):
    h = open('hinglish.txt', 'r')
    stop_words = h.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch number of messages
    temp = df[df['message'] != "<Media omitted>\n"]
    temp = temp[temp['user'] != "group_notification"]
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    frequent_df = pd.DataFrame(Counter(words).most_common(20))
    return frequent_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []

    for message in df['message']:  # Ensure the message is a string
        emojis.extend(c for c in message if c in emoji.EMOJI_DATA)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timel = df.groupby(['year', 'month', 'day']).count()['message'].reset_index()
    time = []
    for i in range(timel.shape[0]):
        time.append(str(timel['day'][i]) + "-" + timel['month'][i] + "-" + str(timel['year'][i]))
    timel['time_day'] = time

    return timel

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap