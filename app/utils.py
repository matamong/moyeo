from datetime import date
from typing import List

# In Progress...
def find_most_overlapping_date(dates: List[date]):
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
    # sorted_dates = sorted(overlap_counts, key=overlap_counts.get, reverse=True)
    sorted_dates = dict(sorted(overlap_counts.items(), key=lambda item: item[1], reverse=True))

    # Find the key and value with the largest integer value
    max_key = most_overlap
    max_value = overlap_counts[max_key]
    keys_with_max_value = []

    for key, value in sorted_dates.items():
        if value > max_value:
            max_key = key
            max_value = value
            keys_with_max_value = [key]
        elif value == max_value:
            keys_with_max_value.append(key)

    print(keys_with_max_value, max_value)

    return most_overlap