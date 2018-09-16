#!/usr/bin python3

import pandas as pd
import numpy as np
import datetime as datetime

def merge_attendance():
    base_CSV = pd.read_csv('../dataset/lpv_d.csv')
    attendance = pd.read_csv('../dataset/provided-data/Attendance_Capacity_Primary_Tickets.csv')
    # for i, row in attendance.iterrows():
    #     attendance.at[i, 'Date'] = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').date()
    # attendance.to_csv('../dataset/provided-data/Attendance_Capacity_Primary_Tickets.csv', index=False)
    merged_df = pd.merge(base_CSV, attendance, how='left', on=['Date', 'Home', 'Away'])
    merged_df.to_csv('../dataset/merge-data/att.csv', index=False)

def merge_dma():
    base_CSV = pd.read_csv('../dataset/merge-data/att.csv')
    dma = pd.read_csv('../dataset/provided-data/DMA_Households.csv')
    base_CSV['dma_home'] = ""
    base_CSV['dma_away'] = ""
    for i, row in base_CSV.iterrows():
        base_CSV.at[i,'dma_home'] = dma.loc[dma['Team'] == row['Home']]['DMA_TV_Households_Millions'].item()
        base_CSV.at[i,'dma_away'] = dma.loc[dma['Team'] == row['Away']]['DMA_TV_Households_Millions'].item()
    base_CSV.to_csv('../dataset/merge-data/att-dma.csv', index=False) 

def merge_national_ratings():
    base_CSV = pd.read_csv('../dataset/merge-data/att-dma.csv')
    nat_rating = pd.read_csv('../dataset/provided-data/National_Ratings_by_Game.csv') 
    # for i, row in nat_rating.iterrows():
    #     nat_rating.at[i, 'Date'] = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').date()
    # attendance.to_csv('../dataset/provided-data/National_Ratings_by_Game.csv', index=False)
    merged_df = pd.merge(base_CSV, nat_rating, how='left', on=['Date', 'Home', 'Away', 'Season'])
    merged_df.to_csv('../dataset/merge-data/att-dma-nat.csv', index=False)

def merge_rsn_rating():
    base_CSV = pd.read_csv('../dataset/merge-data/att-dma-nat.csv')
    rsn_rating = pd.read_csv('../dataset/provided-data/RSN_Ratings_by_Game.csv') 
    merged_df = pd.merge(base_CSV, rsn_rating, how='left', on=['Date', 'Home', 'Away', 'Season'])
    merged_df.to_csv('../dataset/merge-data/att-dma-nat-rsn.csv', index=False)

def merge_secondary_trans():
    base_CSV = pd.read_csv('../dataset/merge-data/att-dma-nat-rsn.csv')
    secondary_trans = pd.read_csv('../dataset/provided-data/Secondary_Transactions_by_Game.csv') 
    merged_df = pd.merge(base_CSV, secondary_trans, how='left', on=['Date', 'Home', 'Away', 'Season'])
    merged_df.to_csv('../dataset/merge-data/att-dma-nat-rsn-sectrans.csv', index=False)

# def merge_velocity():
#     base_CSV = pd.read_csv('../dataset/merge-data/att-dma-nat-rsn-sectrans.csv')
#     velocity = pd.read_csv('../dataset/provided-data/Velocity_of_Individual_Ticket_Sales.csv') 
#     merged_df = pd.merge(base_CSV, velocity, how='left', on=['Season', 'Home', 'Away', 'Date'])
#     merged_df.to_csv('../dataset/merge-data/att-dma-nat-rsn-sectrans-velocity.csv', index=False)

def merge_social():
    base_CSV = pd.read_csv('../dataset/merge-data/att-dma-nat-rsn-sectrans.csv')
    social = pd.read_csv('../dataset/provided-data/New_Social_Media_Metrics.csv')
    for i, row in base_CSV.iterrows():
        date_split = base_CSV.at[i,'Date'].split('-')
        current_year = date_split[0]
        current_month = date_split[1]
        base_CSV.at[i, 'Year'] = int(current_year)
        base_CSV.at[i, 'Month'] = int(current_month)
    
    social.columns = ['Year','Month','Home','Home_Followers_Facebook','Home_Followers_Twitter','Home_Followers_Instagram','Home_Followers_Snapchat','Home_Followers_Weibo','Home_Engagements_Facebook','Home_Engagements_Twitter','Home_Engagements_Instagram','Home_Impressions_Facebook','Home_Impressions_Twitter']
    merged_home = pd.merge(base_CSV, social, how='left', on=['Year', 'Month', 'Home'])
    #merged_home.to_csv('../dataset/merge-data/social-home.csv', index=False)
    # social_home_df = 
    social.columns = ['Year','Month','Away','Away_Followers_Facebook','Away_Followers_Twitter','Away_Followers_Instagram','Away_Followers_Snapchat','Away_Followers_Weibo','Away_Engagements_Facebook','Away_Engagements_Twitter','Away_Engagements_Instagram','Away_Impressions_Facebook','Away_Impressions_Twitter']
    merged_away = pd.merge(merged_home, social, how='left', on=['Year', 'Month', 'Away'])
    merged_away.to_csv('../dataset/merge-data/total-merged.csv', index=False)

def merge_data_set():
    """This function matches and merges CSV to make one data set"""
    # merge_attendance()
    # merge_dma()
    # merge_national_ratings()
    # merge_rsn_rating()
    # merge_secondary_trans()
    merge_social()

merge_data_set()