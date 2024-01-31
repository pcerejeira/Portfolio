import pandas as pd
import numpy as np
from datetime import timedelta
import time

from database.query import fetch_request_logger

def count_and_statistics_by_weekday(df, permission, day_of_week):
    """
    Calculate statistics based on a specific weekday for the provided permission.
    
    Parameters:
    - df: DataFrame with the request data
    - permission: Specific permission to filter the data
    - day_of_week: The day of the week (0=Monday, 6=Sunday)
    
    Returns:
    - final_df: DataFrame with calculated statistics
    """
    permission_df = df[df["permissions"] == permission]
    
    # Convert 'timestamp' column to datetime and extract weekday
    permission_df["timestamp"] = pd.to_datetime(permission_df["timestamp"])
    permission_df["weekday_num"] = permission_df["timestamp"].dt.dayofweek

    # Filter and group by date
    filtered_df = permission_df[permission_df["weekday_num"] == day_of_week]
    grouped = filtered_df.groupby(filtered_df["timestamp"].dt.date).size().reset_index(name="total_requests")

    # Extract required statistics
    max_requests_date = grouped[grouped["total_requests"] == grouped["total_requests"].max()]["timestamp"].values[0]
    total_requests_max_date = grouped[grouped["timestamp"] == max_requests_date]["total_requests"].values[0]
    average_requests = grouped["total_requests"].mean()
    p90 = grouped["total_requests"].quantile(0.9)
    p99 = grouped["total_requests"].quantile(0.99)

    # Create final DataFrame
    final_df = pd.DataFrame({
        "Most_Requests_Date": [max_requests_date],
        "Total_Requests_Most_Date": [total_requests_max_date],
        "Average_Requests": [average_requests],
        "P90_Requests": [p90],
        "P99_Requests": [p99]
    })

    return final_df

def account_requests_by_permission(df, permission):
    """
    Count the number of requests by each account for a specific permission.
    
    Parameters:
    - df: DataFrame with the request data
    - permission: Specific permission to filter the data
    
    Returns:
    - grouped_df: DataFrame with request count per account
    """
    permission_df = df[df["permissions"] == permission]
    grouped_df = permission_df.groupby(["account"]).size().reset_index(name="request_count")
    return grouped_df

def calculate_most_requests_per_day_by_permission(df, permission):
    """
    Calculate which accounts made the most requests in a single day for a specific permission.
    
    Parameters:
    - df: DataFrame with the request data
    - permission: Specific permission to filter the data
    
    Returns:
    - top_10_df: DataFrame with top 10 accounts based on daily requests
    """
    permission_df = df[df["permissions"] == permission]
    permission_df["timestamp"] = pd.to_datetime(permission_df["timestamp"]).dt.date

    # Group by account and timestamp, then calculate required statistics
    grouped_df = permission_df.groupby(["account", "timestamp"]).agg(
        request_count=pd.NamedAgg(column="timestamp", aggfunc="size"),
        time_elapsed_sum=pd.NamedAgg(column="time_elapsed", aggfunc="sum"),
        time_elapsed_max=pd.NamedAgg(column="time_elapsed", aggfunc="max"),
        time_elapsed_avg=pd.NamedAgg(column="time_elapsed", aggfunc="mean"),
        p99_time_elapsed=pd.NamedAgg(column="time_elapsed", aggfunc=lambda x: np.percentile(x, 99)),
        p90_time_elapsed=pd.NamedAgg(column="time_elapsed", aggfunc=lambda x: np.percentile(x, 90))
    ).reset_index()

    # Find the top 10 accounts based on daily request count
    top_10_df = grouped_df.nlargest(10, "request_count")
    return top_10_df

# ... [rest of the imports and functions unchanged]

def project_4(timestamp_start, timestamp_end, output_path="/temp"):
    """
    Fetch and analyze request_logger data for specific paths between two timestamps.
    
    Parameters:
    - timestamp_start: Starting timestamp for data fetching
    - timestamp_end: Ending timestamp for data fetching
    - output_path: Path where to save the final analysis CSV
    
    Returns:
    - None. Saves a CSV file and prints statistics.
    """
    start = time.time()
    df_final = pd.DataFrame()

    # Fetch data in chunks of 5 days
    timestamp_aux = timestamp_start + timedelta(days=5)
    while timestamp_aux <= timestamp_end:
        timestamp_begin = timestamp_aux - timedelta(days=5)
        df = fetch_request_logger(timestamp_begin, timestamp_aux, "raw-records-for-plot")
        df_final = pd.concat([df_final, df], ignore_index=True)
        timestamp_aux += timedelta(days=5)

    # Filter data based on specific paths, analyzing /raw-records-for-plot path
    is_raw = df_final["path"].str.contains(r".*/raw-records-for-plot$")
    raw_records_df = df_final[is_raw]

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for idx, day in enumerate(weekdays):
        daily_stats = count_and_statistics_by_weekday(raw_records_df, "partner", idx)
        print(f"Statistics for {day}:", daily_stats)

    admin_stats = calculate_most_requests_per_day_by_permission(raw_records_df, "admin")
    print("Maximum daily requests by an admin account:", admin_stats)

    partner_stats = calculate_most_requests_per_day_by_permission(raw_records_df, "partner")
    print("Maximum daily requests by a partner account:", partner_stats)

    partner_requests = account_requests_by_permission(raw_records_df, "partner")
    print("Requests by partner accounts:", partner_requests)

    licensee_requests = account_requests_by_permission(raw_records_df, "licensee")
    print("Requests by licensee accounts:", licensee_requests)

    # Save final results
    df_final.to_csv(f"{output_path}/RequestLoggerAnalysis.csv", index=False)

    end = time.time()
    print(f"Total execution time: {end - start} seconds")

