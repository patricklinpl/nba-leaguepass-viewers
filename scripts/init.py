#!/usr/bin python3

import pandas as pd
import numpy as np
import datetime as datetime

def changeDate():
    base_CSV = pd.read_csv('../dataset/lpv_d.csv')
    target = pd.read_csv('')
    for i, row in target.iterrows():
        target.at[i, 'Date'] = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').date()
    target.to_csv('', index=False)

def merge_attendance():
    base_CSV = pd.read_csv('../dataset/lpv_d.csv')
    attendance = pd.read_csv('../dataset/provided-data/Attendance_Capacity_Primary_Tickets.csv')
    merged_df = pd.merge(base_CSV, attendance, how='left', on=['Date', 'Home', 'Away'])
    for i, row in merged_df.iterrows():
        merged_df.at[i, 'Season'] = '2017-18'
        
    return merged_df

def merge_dma(df):
    dma = pd.read_csv('../dataset/provided-data/DMA_Households.csv')
    for i, row in df.iterrows():
        df.at[i,'dma_home'] = dma.loc[dma['Team'] == row['Home']]['DMA_TV_Households_Millions'].item()
        df.at[i,'dma_away'] = dma.loc[dma['Team'] == row['Away']]['DMA_TV_Households_Millions'].item()
    return df

def merge_national_ratings(df):
    nat_rating = pd.read_csv('../dataset/provided-data/National_Ratings_by_Game.csv') 
    return pd.merge(df, nat_rating, how='left', on=['Date', 'Home', 'Away', 'Season']) 

def merge_rsn_rating(df):
    rsn_rating = pd.read_csv('../dataset/provided-data/RSN_Ratings_by_Game.csv') 
    return pd.merge(df, rsn_rating, how='left', on=['Date', 'Home', 'Away', 'Season'])

def merge_secondary_trans(df):
    secondary_trans = pd.read_csv('../dataset/provided-data/Secondary_Transactions_by_Game.csv') 
    return pd.merge(df, secondary_trans, how='left', on=['Date', 'Home', 'Away', 'Season'])

def merge_social(df):
    social = pd.read_csv('../dataset/provided-data/New_Social_Media_Metrics.csv')
    for i, row in df.iterrows():
        date_split = df.at[i,'Date'].split('-')
        current_year = date_split[0]
        current_month = date_split[1]
        df.at[i, 'Year'] = int(current_year)
        df.at[i, 'Month'] = int(current_month)
    social.columns = ['Year','Month','Home','Home_Followers_Facebook','Home_Followers_Twitter','Home_Followers_Instagram','Home_Followers_Snapchat','Home_Followers_Weibo','Home_Engagements_Facebook','Home_Engagements_Twitter','Home_Engagements_Instagram','Home_Impressions_Facebook','Home_Impressions_Twitter']
    merged_home = pd.merge(df, social, how='left', on=['Year', 'Month', 'Home'])
    social.columns = ['Year','Month','Away','Away_Followers_Facebook','Away_Followers_Twitter','Away_Followers_Instagram','Away_Followers_Snapchat','Away_Followers_Weibo','Away_Engagements_Facebook','Away_Engagements_Twitter','Away_Engagements_Instagram','Away_Impressions_Facebook','Away_Impressions_Twitter']
    merged_away = pd.merge(merged_home, social, how='left', on=['Year', 'Month', 'Away'])
    merged_away.to_csv('../dataset/total-merged.csv', index=False)

def merge_data_set():
    """This function matches and merges CSV to make one data set"""
    df_att = merge_attendance()
    df_dma = merge_dma(df_att)
    df_nat = merge_national_ratings(df_dma)
    df_rsn = merge_rsn_rating(df_nat)
    df_sec = merge_secondary_trans(df_rsn)
    merge_social(df_sec)

merge_data_set()