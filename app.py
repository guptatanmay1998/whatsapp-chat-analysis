import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import helper
import preprocessor
st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file=st.sidebar.file_uploader('Upload Chats')

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    #st.text(data)
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    users_list=df['users'].unique().tolist()
    users_list.remove('group notification')
    users_list.sort()
    users_list.insert(0,'overall')
    selected_user=st.sidebar.selectbox('Show Analysis wrt',users_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,num_words,num_media,num_links=helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header('Total Messages:')
            st.title(num_messages)

        with col2:
            st.header('Total Words:')
            st.title(num_words)

        with col3:
            st.header('Total Media Files:')
            st.title(num_media)

        with col4:
            st.header('Total Links:')
            st.title(num_links)

            # monthly timeline

#find most active user in group-
        if selected_user=='overall':
            col1,col2=st.columns(2)
            with col1:
                st.header('User Activity:bar plot')
                #st.title()
                x=helper.fetch_busy_users(df)
                fig=plt.figure(figsize=(14,10))
                plt.bar(x.index,x.values)
                plt.xticks(rotation='vertical',fontsize=25)
                plt.yticks(fontsize=25)
                st.pyplot(fig)
            with col2:
                st.header('User Activity:pie chart')
                x = df['users'].value_counts()
                fig = plt.figure(figsize=(30, 15))
                x.plot(kind='pie', autopct='%.1f', fontsize=30)
                st.pyplot(fig)
        #make wordcloud
        df_wc=helper.wordcloud(selected_user,df)
        fig=plt.figure(figsize=(15,10))
        plt.imshow(df_wc)
        st.pyplot(fig)
        #most common 20 words
        stopwords,df_most_common=helper.most_common_words(selected_user,df)
        #st.dataframe(df_most_common)
        fig=plt.figure(figsize=(30,10))
        plt.barh(df_most_common[0],df_most_common[1])
        plt.xticks(rotation='vertical',fontsize=25)
        plt.yticks(fontsize=30)
        st.pyplot(fig)
        #st.text(stopwords)

        #emoji analysis
        st.header('Emoji Analysis')
        emoji_df=helper.emoji_helper(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig=plt.figure(figsize=(30,10))
            plt.pie(emoji_df[1],labels=emoji_df[0],autopct='%.2f')
            plt.xticks(fontsize=30)
            st.pyplot(fig)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



