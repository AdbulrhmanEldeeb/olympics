import numpy as np
import streamlit as st 
import pandas as pd 

import seaborn as sns 


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def preprocess_over_time(df, entity):
    if entity not in ['region', 'Event','Name']:
        raise ValueError("Entity must be 'region' or 'Event'or 'Name' ")

    unique_over_time = df.drop_duplicates(['Year', entity])['Year'].value_counts().sort_values()
    unique_over_time = pd.DataFrame(unique_over_time).sort_values('Year')
    unique_over_time['year'] = unique_over_time.index
    
    if entity == 'region':
        unique_over_time.rename(columns={'count': 'No of countries'}, inplace=True)
    elif entity == 'Name' : 
        unique_over_time.rename(columns={'count': 'No of Athletes'}, inplace=True)
    else:
        unique_over_time.rename(columns={'count': 'No of events'}, inplace=True)
    
    return unique_over_time

def get_most_successful(all_df,sport): 
    all_df['total']=all_df['Gold']+all_df['Silver']+all_df['Bronze']
    temp_df = all_df.dropna(subset=['Medal'])

    if sport=='Overall': 
        
        
        most_winning_medals_players=temp_df.groupby('Name')['total'].sum().sort_values(ascending=False)[:10]
        
        top_players = most_winning_medals_players.reset_index()

        # Rename the columns for clarity
        top_players = top_players.rename(columns={'index': 'Name', 'total': 'Number of Medals'})

        # Now, let's merge this with the original DataFrame to get the Sport and Region
        result_df = top_players.merge(temp_df[['Name', 'Sport', 'region']], on='Name', how='left')

        # Drop duplicates to keep only one row per athlete
        result_df = result_df.drop_duplicates(subset=['Name'])

        # Select and reorder the columns we want
        result_df = result_df[['Name', 'Number of Medals', 'Sport', 'region']]
        return result_df

    else : 
        most_winning_medals_players=temp_df[temp_df['Sport']==sport].groupby('Name')['total'].sum().sort_values(ascending=False)[:10]
        most_winning_medals_players
        top_players = most_winning_medals_players.reset_index()

        # Rename the columns for clarity
        top_players = top_players.rename(columns={'index': 'Name', 'total': 'Number of Medals'})

        # Now, let's merge this with the original DataFrame to get the Sport and Region
        result_df = top_players.merge(temp_df[['Name', 'Sport', 'region']], on='Name', how='left')

        # Drop duplicates to keep only one row per athlete
        result_df = result_df.drop_duplicates(subset=['Name'])

        # Select and reorder the columns we want
        result_df = result_df[['Name', 'Number of Medals', 'Sport', 'region']]
        return result_df

def years_wise_medal_tally(df,country): 

    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    medal_line_plot=new_df.groupby('Year')['Medal'].count().sort_index()
    new_df_1=pd.DataFrame(medal_line_plot)
    new_df_1['Year']=new_df_1.index
    return new_df_1 


def sports_years_heatmap(df,country): 
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally_1=medal_df[medal_df['region']==country]
    medal_tally_1_pivot=medal_tally_1.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)

    heatmap=sns.heatmap(medal_tally_1_pivot,annot=True)

    return heatmap


def most_successful_players_countrywise(df, country):
    # Filter out rows where 'Medal' is NaN and select rows where 'region' is the specified country
    temp_df_1 = df.dropna(subset=['Medal'])
    temp_df_1 = temp_df_1[temp_df_1['region'] == country]

    # Group by 'Name' and count the number of medals for the top 10 players
    x_1 = temp_df_1.groupby('Name')['Medal'].count().sort_values(ascending=False).head(10).reset_index()
    x_1 = x_1.merge(df, on='Name', how='left')[['Name', 'Medal_x', 'Sport']].drop_duplicates()
    x_1.rename(columns={'Medal_x': 'Total Medals'}, inplace=True)
    
    # Initialize an empty DataFrame to store medal counts
    medals_df = pd.DataFrame(columns=['Name', 'Gold', 'Silver', 'Bronze'])

    # Calculate the number of Gold, Silver, and Bronze medals for each player
    for name in x_1['Name'].tolist():
        medals = df[df['Name'] == name].groupby('Name')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
        medals_df = pd.concat([medals_df, medals], axis=0)

    # Merge the medal counts with the top 10 players DataFrame
    final_df = x_1.merge(medals_df, on='Name', how='left').drop_duplicates()

    return final_df    



def age_dist_plot_by_sport(df,sport): 
    
    # Filter the data
    atlete_df = df.drop_duplicates(subset=['Name', 'region'])
    atlete_df=atlete_df[atlete_df['Sport']==sport]
    gold_df = atlete_df[atlete_df['Medal'] == 'Gold']
    silver_df = atlete_df[atlete_df['Medal'] == 'Silver']
    bronze_df = atlete_df[atlete_df['Medal'] == 'Bronze']

    # Create distribution plots
    age_distribution = atlete_df['Age'].dropna()
    gold_age_distribution = gold_df['Age'].dropna()
    silver_age_distribution = silver_df['Age'].dropna()
    bronze_age_distribution = bronze_df['Age'].dropna()

    # Combine the data
    hist_data = [age_distribution, gold_age_distribution, silver_age_distribution, bronze_age_distribution]
    group_labels = ['Overall Age Distribution', 'Gold medal winners Age Distribution', 'Silver medal winners Age Distribution', 'Bronze medal winners Age Distribution']

    # Create the combined distribution plot
    
    return hist_data , group_labels 

most_famous_sports = [
    'Basketball',
    'Judo',
    'Football',
    'Athletics',
    'Swimming',
    'Gymnastics',
    'Handball',
    'Weightlifting',
    'Wrestling',
    'Boxing',
    'Tennis',
    'Cycling',
    'Volleyball',
    'Hockey',
    'Rowing'
]

def sports_ages_dist_plot(df, most_famous_sports):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    age_dists = []
    labels = []
    for sport in most_famous_sports:
        custom_df = medal_df[medal_df['Sport'] == sport].dropna(subset=['Age'])
        age_dist = custom_df['Age'].tolist()
        age_dists.append(age_dist)
        labels.append(sport)
    return age_dists, labels

def men_women_line_plot(df): 
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    men_df=medal_df[medal_df['Sex']=='M']
    men_df=pd.DataFrame(men_df.groupby('Year')['ID'].count().sort_index())
    men_df['Year']=men_df.index

    women_df=medal_df[medal_df['Sex']=='F']
    women_df=pd.DataFrame(women_df.groupby('Year')['ID'].count().sort_index())
    women_df['Year']=women_df.index

    return men_df,women_df
