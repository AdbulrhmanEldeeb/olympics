import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.graph_objects as go


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    # plot of nations over years 
    nations_over_time = helper.preprocess_over_time(df,entity='region')
    fig=px.line(nations_over_time,x='year',y='No of countries')
    fig.update_traces(line=dict(color='#131842', width=2), marker=dict(size=10, color='red', symbol='circle'))

    fig.update_layout(
    title={'text': 'Number of Participating Nations Over the Years', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Year',
    yaxis_title='Number of Countries',
    font=dict(family='Arial, sans-serif', size=14, color='black'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
)

    st.title("Participating Nations over the years")
    st.plotly_chart(fig)




    # plot of events over years 
    events_over_time = helper.preprocess_over_time(df, entity='Event')
    fig=px.line(events_over_time,x='year',y='No of events')
    fig.update_traces(line=dict(color='#2F3645', width=2), marker=dict(size=10, color='red', symbol='circle'))

    fig.update_layout(
    title={'text': 'Number of Events Over the Years', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Year',
    yaxis_title='Number of Events',
    font=dict(family='Arial, sans-serif', size=14, color='black'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
)

    st.title("Events over the years")
    st.plotly_chart(fig)


    # plot of athlete of time 

    athlete_over_time  = helper.preprocess_over_time(df, entity='Name')
    fig=px.line(athlete_over_time ,x='year',y='No of Athletes')
    fig.update_traces(line=dict(color='#088395', width=2), marker=dict(size=10, color='red', symbol='circle'))

    fig.update_layout(
    title={'text': 'Number of Athletes Over the Years', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Year',
    yaxis_title='Number of Athletes',
    font=dict(family='Arial, sans-serif', size=14, color='black'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
)

    st.title("Athletes over the years")
    st.plotly_chart(fig)

    # heatmap of Events over time(Every Sport)
    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sports_events_count_over_years=x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count')
    sports_events_count_over_years.fillna(0,inplace=True)
    ax=sns.heatmap(sports_events_count_over_years,annot=True)

    st.pyplot(fig)
    

    # getting dataframes of most successfull players 

    all_sports = df['Sport'].unique()
    all_sports = all_sports.tolist()
    all_sports.insert(0, 'Overall')  # This modifies the list in place
    st.title("Players who won most medals in each Sport")
    selected_sport = st.selectbox('Select a sport', all_sports)
    best_players_df=helper.get_most_successful(df,sport=selected_sport)
    st.table(best_players_df)

if user_menu == 'Country-wise Analysis': 

    st.sidebar.title('Country-wise Analysis')
    # country wise analysis of medal tally 

    st.title('Medal tally over years by country')
    country = helper.country_year_list(df)[1]
    selected_country_1=st.sidebar.selectbox('Select a country',country[1:],index=191)
    st.header(selected_country_1 + " Medal Tally over the years")
    medals_over_years=helper.years_wise_medal_tally(df,selected_country_1)

    fig=px.line(medals_over_years,x='Year',y='Medal')
    fig.update_traces(line=dict(color='#088395', width=2), marker=dict(size=10, color='red', symbol='circle'))

    fig.update_layout(
    title={'text': 'Number of Medals Tally Over the Years', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Year',
    yaxis_title='Number of Medals',
    font=dict(family='Arial, sans-serif', size=14, color='black'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
)

    st.plotly_chart(fig)

    # heatmap of medal tally for different sports over years for each country 

    st.title(f'Medal tally of Sports for {selected_country_1} over years')

    fig,ax = plt.subplots(figsize=(25,25))
    
    ax=helper.sports_years_heatmap(df,selected_country_1)

    st.pyplot(fig)
    

    most_successfull_countrywise=helper.most_successful_players_countrywise(df,selected_country_1)
    st.title(f'Most Successfull players in {selected_country_1} in history of olympics')
    st.table(most_successfull_countrywise)

if user_menu == 'Athlete wise Analysis': 
    
    all_sports = df['Sport'].unique()
    all_sports = all_sports.tolist()
    selected_sport_1 = st.selectbox('Select a sport', all_sports[1:],index=4)
    st.title(f'Dist plot of ages of medal winners for {selected_sport_1}')

    hist_data,group_labels=helper.age_dist_plot_by_sport(df,selected_sport_1)
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)

    # Update layout
    fig.update_layout(title=f'Age Distribution of Athletes and Medal Winners for {selected_sport_1}')

    st.plotly_chart(fig)
    
  
    most_famous_sports = ['Basketball', 'Judo', 'Football', 'Athletics', 'Swimming', 'Gymnastics', 'Boxing', 'Tennis', 'Shooting', 'Weightlifting', 'Wrestling', 'Rowing', 'Cycling', 'Fencing', 'Handball']

    age_dists, labels = helper.sports_ages_dist_plot(df, most_famous_sports)
    fig = ff.create_distplot(age_dists, labels, show_hist=False, show_rug=False)
    st.title("Age Distribution of Athletes in the Most Famous Olympic Sports")

    st.plotly_chart(fig)

    men_df,women_df=helper.men_women_line_plot(df)

    fig = go.Figure()

    # Add men's data
    fig.add_trace(go.Scatter(x=men_df['Year'], y=men_df['ID'], mode='lines', name='Men'))

    # Add women's data
    fig.add_trace(go.Scatter(x=women_df['Year'], y=women_df['ID'], mode='lines', name='Women'))

    # Update the layout
    fig.update_layout(
        
        xaxis_title='Year',
        yaxis_title='Number of Medals',
        legend_title='Gender'
)
    st.title('Number of Medals Won by Men and Women Over the Years')
    st.plotly_chart(fig)

