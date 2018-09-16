#!/usr/bin python3

import pandas as pd
import numpy as np
import datetime as datetime

def merge_attendance():
    base_CSV = pd.read_csv('../dataset/lpv_d2.csv')
    attendance = pd.read_csv('../dataset/provided-data/Attendance_Capacity_Primary_Tickets.csv')
    for i, row in attendance.iterrows():
        attendance.at[i, 'Date'] = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').date()

    # attendance.to_csv('../dataset/merge-data/attendance.csv', index=False)


def merge_data_set():
    """This function matches and merges CSV to make one data set"""
    merge_attendance()


merge_data_set()