from datetime import date, datetime
from typing import List
import pandas as pd


def find_most_overlapping_dates(dates: List[date]):
    start_date = min(dates)  
    end_date = max(dates)
    overlap_counts = {}

    for d in dates:
        if start_date <= d <= end_date:
            if d in overlap_counts:
                overlap_counts[d] += 1
            else:
                overlap_counts[d] = 1
    
    most_overlap = max(overlap_counts, key=overlap_counts.get)

    max_key = most_overlap
    max_value = overlap_counts[max_key]
    keys_with_max_value = []

    for key, value in overlap_counts.items():
        if value > max_value:
            max_key = key
            max_value = value
            keys_with_max_value = [key]
        elif value == max_value:
            keys_with_max_value.append(key)
    
    return keys_with_max_value


def find_most_overlapping_datetimes(datetimes: List[str]):
    df = pd.DataFrame({'Datetime': datetimes})
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    datetime_counts = df['Datetime'].value_counts()
    most_overlapping_datetime = datetime_counts.idxmax()
    return most_overlapping_datetime

