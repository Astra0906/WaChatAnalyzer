
from urlextract import  URLExtract
from wordcloud import WordCloud
from collections import Counter
import  pandas as pd
import emoji
def fetch_sts(s_user,df):
    words=[]
    urls=[]
    extract=URLExtract()
    if s_user!="Overall":
        df=df[df['user']==s_user]

    for dm in df['message']:
        url=extract.find_urls(dm)
        urls.extend(url)
        words.extend(dm.split( ))

    num_m=df[df['message']=='<Media omitted>\n'].shape[0]
    new_df=df
    new_df.drop_duplicates(subset=['date'])

    return df.shape[0],len(words),num_m,len(urls),new_df.shape[0]


def fetch_act_bar(df):
    bar_crt=df['user'].value_counts()
    bar_crt.sort_values(ascending=False)
    bar=round(bar_crt/df.shape[0]*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return bar_crt,bar

def create_wc(s_user,df1):
    if s_user != "Overall":
        df1 = df1[df1['user'] == s_user]
    df1 = df1[df1['user'] != 'Notification']
    temp = df1[df1['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "This message was deleted\n"]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

def most_used_words(s_user,df1):
    f = open('stop_hinglish.txt', 'r')
    stop_wrd = f.read()

    if s_user!="Overall":
        df1=df1[df1['user']==s_user]
    df1 = df1[df1['user'] != 'Notification']
    temp = df1[df1['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "This message was deleted\n"]

    word = []
    for dm in temp['message']:
        for wrds in dm.lower().split():
            if wrds not in stop_wrd:
                word.append(wrds)

    return pd.DataFrame(Counter(word).most_common(15))

def emoji_lst(s_user,df):
    if s_user!="Overall":
        df=df[df['user']==s_user]

    emojis=[]
    for dm in df['message']:
        emojis.extend(list(emoji.distinct_emoji_list(dm)))

    emo_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emo_df

def month_timeLine(s_user,df):
    if s_user!="Overall":
        df=df[df['user']==s_user]


    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    m_time = []
    for i in range(timeline.shape[0]):
        m_time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['m_time'] = m_time
    return  timeline

def daily_time(s_user,df):
    if s_user!="Overall":
        df=df[df['user']==s_user]
    d_time = df.groupby(['o_date']).count()['message'].reset_index()
    return pd.DataFrame(d_time)

def activity_map(s_user,df):
    if s_user!="Overall":
        df=df[df['user']==s_user]

    act_day=df.groupby(['day_name']).count()['message'].reset_index()
    act_month=df.groupby(['month']).count()['message'].reset_index()
    return act_day.set_index('day_name'),act_month.set_index('month')


def h_map(s_user,df):
    if s_user!="Overall":
        df=df[df['user']==s_user]

    act_hmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return act_hmap



