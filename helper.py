import pandas as pd
import string
import numpy as np
import matplotlib.pyplot as plt
import emoji
from wordcloud import WordCloud
from collections import Counter
#%matplotlib inline
from urlextract import URLExtract
extractor=URLExtract()
def fetch_stats(selected_user,df):
    words = []
    links=[]
    if selected_user=='overall':
        total_messages=len(df)
        for message in df['messages']:
            words.extend(message.split())
            links.extend(extractor.find_urls(message))
        total_words=len(words)
        total_media=len(df[df['messages']=='<Media omitted>\n'])
        total_links=len(links)
    else:
        total_messages=df.groupby('users').count().loc['{}'.format(selected_user)].messages
        for message in df[df['users']==selected_user]['messages']:
            words.extend(message.split())
            links.extend(extractor.find_urls(message))
        total_words=len(words)
        new_df=df[df['users']==selected_user]
        total_media = len(new_df[new_df['messages'] == '<Media omitted>\n'])
        total_links = len(links)
        #total_messages=df.groupby('users')['{}'.format(selected_user)].count()

    return total_messages,total_words,total_media,total_links

def fetch_busy_users(df):
    #top 5 busy users
    x=df['users'].value_counts().head()
    return x
    # plt.bar(x.index,x.values)
    # plt.xticks(rotation='vertical')
    # plt.show()
def wordcloud(selected_user,df):
    if selected_user!='overall':
        df=df[df['users']==selected_user]
    wc=WordCloud(height=500,width=500,background_color='black',min_font_size=10)
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()
    temp = df[df['users'] != 'group notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            word = word.translate(str.maketrans('', '', string.punctuation))
            if word not in stopwords:
                words.append(word)
    df_wc=wc.generate(' '.join(words))
    #df_wc=wc.generate(pd.Series([message for message in df['messages'] if message!='<Media omitted>\n']).str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stopwords=f.read()
    if selected_user!='overall':
        df=df[df['users']==selected_user]

    temp=df[df['users']!='group notification']
    temp=temp[temp['messages']!='<Media omitted>\n']
    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            word = word.translate(str.maketrans('', '', string.punctuation))
            if word not in stopwords:
                #word=word.translate(str.maketrans('', '', string.punctuation))
                words.append(word)
    return stopwords,pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user,df):
    if selected_user!='overall':
        df=df[df['users']==selected_user]

    emojis=[]
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emojis_df=pd.DataFrame(Counter(emojis).most_common(20))
    return emojis_df

def monthly_timeline(selected_user,df):
    if selected_user!='overall':
        df=df[df['users']==selected_user]
    df['month_num']=df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]
    df['only_date']=df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]
    df['day_name']=df['date'].dt.day_name()
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap




