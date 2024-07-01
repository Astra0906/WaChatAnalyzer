import pandas as pd
import streamlit as st
import preprocessor,helper
import  matplotlib.pyplot as plt
import  seaborn as sns

st.sidebar.title("WA chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload chat export file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    user_list=df['user'].unique().tolist()

    if 'Notification' in user_list:
        user_list.remove('Notification')

    user_list.sort()
    user_list.insert(0,"Overall")
    s_user=st.sidebar.selectbox("Analysis wrt user",user_list)
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        col1,col2,col3,col4= st.columns([1,1.2,1,1],vertical_alignment="bottom",gap='small')

        num_dm,num_word,media,num_url,act_days=helper.fetch_sts(s_user,df)

        with col1:
            st.subheader('total messages')
            st.title(num_dm)

        with col2:
            st.subheader('total Words used')
            st.title(num_word)

        with col3:
            st.subheader('total media shared')
            st.title(media)

        with col4:
            st.subheader('total Link shared')
            st.title(num_url)


        #TIMLINE
        st.title("Monthly Timeline")
        timeline=helper.month_timeLine(s_user,df)
        timeline=timeline.set_index('m_time')

        st.line_chart(timeline['message'])


        st.title("Daily Timeline")
        d_time=helper.daily_time(s_user,df)
        d_time=d_time.set_index('o_date')
        st.line_chart(d_time)

        st.title("Activity Map")
        col1,col2=st.columns(2,gap='large')
        act_day,act_month=helper.activity_map(s_user,df)

        with col1:
            st.subheader("Busy Days")
            st.bar_chart(act_day)

        with col2:
            st.subheader("Busy Months")
            st.bar_chart(act_month)

        #HEATMAp
        st.title("Weekly activity map")
        h_map=helper.h_map(s_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(h_map)

        st.pyplot(fig)



        #fethcing the activity of thevhe user

        if s_user=="Overall":
            st.title("Most busy Users ")

            col1,col2=st.columns([1.4,1],gap='medium',vertical_alignment='bottom')
            source,bar=helper.fetch_act_bar(df)

            with col1:
                st.write("Bar chart ")
                st.bar_chart(source.head())

            with col2:
                st.write("activity table")
                st.dataframe(bar)

        #wordcloud
        df_wc=helper.create_wc(s_user,df)
        st.title("WordCloud")

        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most used words
        st.title("Most common words")
        x=helper.most_used_words(s_user,df)
        words = pd.DataFrame({'txt': x.iloc[:, 0], 'count': x.iloc[:, 1]})
        words=words.set_index('txt')

        st.bar_chart(words,horizontal=True)

        #EMOJI analyze
        emo_df=helper.emoji_lst(s_user,df)
        st.title("Emoji Analysis")
        if emo_df.shape[0]==0:
            st.write(" There is no emojis")
        else:

            col1, col2 = st.columns([1,1.7],vertical_alignment='bottom')
            with col1:

                st.dataframe(emo_df)

            with col2:
                st.subheader('Pie chart')
                plt.style.use('dark_background')
                plt.rcParams['font.family']='Noto'

                fig, ax = plt.subplots()

                ax.pie(emo_df[1].head(), labels=emo_df[0].head(), autopct="%0.2f")

                st.pyplot(fig)






















