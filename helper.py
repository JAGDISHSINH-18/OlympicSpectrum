import numpy as np


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

def data_over_time(df,col):
        # Drop duplicates to consider unique instances of 'Year' and the specified column
        temp_df = df.drop_duplicates(['Year', col])

        # Count the unique values for each 'Year'
        nations_over_time = temp_df['Year'].value_counts().reset_index()

        # Rename the columns to provide meaningful names
        nations_over_time.columns = ['Edition', col]

        # Sort by the 'Edition' (Year) column
        nations_over_time = nations_over_time.sort_values('Edition')

        return nations_over_time


def most_successful(df, sport):
    # Filter out rows without medals
    temp_df = df.dropna(subset=['Medal'])

    # Filter by the specific sport if one is selected
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Get the top 15 most successful athletes
    athlete_medals = temp_df['Name'].value_counts().reset_index().head(15)
    athlete_medals.columns = ['Name', 'Medals']  # Rename columns to make merging clearer

    # Merge to get additional athlete details
    merged_df = athlete_medals.merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Medals', 'Sport', 'region']]

    # Remove any duplicate entries to avoid repetition
    merged_df = merged_df.drop_duplicates('Name')

    return merged_df


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    # Filter the dataframe to include only rows where the 'Medal' column is not null
    temp_df = df.dropna(subset=['Medal'])

    # Filter by the specific country
    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 10 most successful athletes from the country
    athlete_medals = temp_df['Name'].value_counts().reset_index().head(10)
    athlete_medals.columns = ['Name', 'Medals']  # Rename columns to avoid ambiguity

    # Merge with the original DataFrame to get additional details
    merged_df = athlete_medals.merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'Medals', 'Sport']]

    # Remove duplicate entries to avoid repetition
    merged_df = merged_df.drop_duplicates('Name')

    return merged_df


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final