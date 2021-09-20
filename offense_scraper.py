import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import os
import datetime

# select all option to get all rows in stats.nba.com table
def select_all(driver):
    select_options = driver.find_elements_by_xpath("//select")
    try:
        for s in select_options:
            select_test = Select(s)
            for option in select_test.options:
                if 'All' == option.text:
                    dropdown_menu = select_test
                    dropdown_menu.select_by_visible_text('All')
    except Excpetion as e:
        print("Error selecting all...")
        print(f"{err}")
        quit()

# convert feet-inch to inches
def get_height(x):
    return int(x.split('-')[0]) * 12 + int(x.split('-')[1])

def main(season):
    # make sure raw_data/season exists
    try:
        os.mkdir(f'final_data/{season}')
        print(f"Generated dir final_data/{season}")
    except Exception as e:
        print(f"Dir final_data/{season} already exists")

    # get the url set for all the players
    driver = webdriver.Chrome('./chromedriver')
    driver.get(f'https://www.nba.com/stats/players/bio/?Season={season}&SeasonType=Regular%20Season')
    select_all(driver)

    # get player team/age/height/weight
    df = pd.read_html(driver.page_source)[0]
    df = df[['Player', 'Team', 'Age', 'Height', 'Weight']]
    df.dropna(inplace=True)

    # get the games played and minutes
    driver.get(f'https://www.nba.com/stats/players/traditional/?sort=PTS&dir=-1&Season={season}&SeasonType=Regular%20Season&PerMode=Totals')
    select_all(driver)
    df2 = pd.read_html(driver.page_source)[0]
    df2 = df2[['PLAYER', 'TEAM', 'GP', 'MIN']]
    final_df = pd.merge(df, df2, left_on=['Player', 'Team'], right_on=['PLAYER','TEAM'])
    final_df.drop(columns=['PLAYER', 'TEAM'], inplace=True)

    # get all offensive synergy stats for every players
    type = [
        'isolation',
        'transition',
        'ball-handler',
        'roll-man',
        'playtype-post-up',
        'spot-up',
        'hand-off',
        'cut',
        'off-screen',
        'putbacks'
    ]


    poss_cols = []
    for t in type:
        while True:
            driver.get(f'https://www.nba.com/stats/players/{t}/?SeasonType=Regular%20Season&SeasonYear={season}&PerMode=Totals')
            select_all(driver)
            temp = pd.read_html(driver.page_source)[0]
            temp = temp[['Player', 'Poss', 'PTS']]
            temp = temp.groupby('Player', as_index=False).agg('sum')

            if temp.shape[0] > 50:
                temp = temp.rename(columns = {'Poss': f"{t}_poss", "PTS": f"{t}_pts"})
                poss_cols.append(f"{t}_poss")
                final_df = pd.merge(final_df, temp, on='Player', how='left')
                break

    # add frequency, points per possession, and percentiles
    final_df['poss'] = final_df[poss_cols].sum(axis=1)
    for t in type:
        final_df[f'{t}_ppp'] = final_df[f'{t}_pts'] / final_df[f'{t}_poss']
        final_df[f'{t}_percentile'] = final_df[f'{t}_ppp'].rank(pct=True)
        final_df[f'{t}_freq'] = final_df[f'{t}_poss'] / final_df['poss']

    final_df.fillna(-100, inplace=True)

    #final_df = pd.merge(final_df, df3, left_on=['Player', 'Team'], right_on=['Player','Team'])
    final_df['Height'] = final_df['Height'].apply(get_height)

    # save to final location
    print(final_df)
    print(final_df.shape)
    final_df.to_csv(f'final_data/{season}/offense.csv', index=False)

    return final_df.shape

if __name__ == '__main__':
    while True:
        shape = main(sys.argv[1])
        if shape[0] > 50:
            break
