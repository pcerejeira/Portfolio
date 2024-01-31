import pandas as pd
import numpy as np
from database import fetch_vehicle_from_client, fetch_vehicle_operation
from datetime import timedelta

"""
Goal: Fetch all stops (non-facilities) from given vehicles (fetching vehicles by each client)
"""

def proj_2(timestamp_start, timestamp_end, client, output_path='/temp'):
    vehicles = fetch_vehicle_from_client(client)
    df_final = pd.DataFrame(columns=['vehicle', 'registered_at', 'latitude', 'longitude', 'is_in_facilities', 'vehicle_is_stopped'])
    
    # Fetching data in 15-day intervals from the vehicle_operation table
    for vehicle in vehicles:
        timestamp_aux = timestamp_start + timedelta(days=15)
        while timestamp_aux != (timestamp_end + timedelta(days=15)):
            timestamp_begin = timestamp_aux - timedelta(days=15)
            if timestamp_aux >= timestamp_end:
                timestamp_aux = timestamp_end
            df = fetch_vehicle_operation(vehicle, timestamp_begin, timestamp_aux)
            df_final = pd.concat([df_final, df])
            timestamp_aux += timedelta(days=15)
    
    df_final = df_final.drop(columns=['registered_at', 'vehicle_is_stopped'])
    df_final = df_final.round({'latitude': 3, 'longitude': 3})

    # Grouping stops by vehicle and respective coordinates, counting the number of occurrences
    df_final = df_final.groupby(['vehicle', 'latitude', 'longitude']).count()
    df_final.rename(columns={'is_in_facilities': 'records'}, inplace=True)

    # Cleaning data, dropping non-significant stops and default/error values
    df_data = df_final
    df_data = df_data.reset_index(drop=False)
    df_data = df_data[df_data.records > 50]
    df_data = df_data[df_data.latitude != 0]
    df_data = df_data[df_data.longitude != 0]

    df_data["vehicle_count"] = 1
    df_data["vehicle_list"] = ""

    # Considering nearby coordinates as the same (within a range of 0.003), based on https://en.wikipedia.org/wiki/Decimal_degrees
    # Grouping all stops by latitude and longitude, saving the number of occurrences as "records" and the related vehicle IDs in "vehicle_list"
    df_data = df_data.reset_index(drop=True)
    for v in range(0, len(df_data) - 1):
        if v > len(df_data) - 1:
            break
        aux_vehicle = [df_data["vehicle"][v]]
        for i in range(v + 1, len(df_data) - 1):
            if (df_data["latitude"][v] - 0.003 <= df_data["latitude"][i] <= df_data["latitude"][v] + 0.003 and df_data["longitude"][v] - 0.003 <= df_data["longitude"][i] <= df_data["longitude"][v] + 0.003):
                df_data["records"][v] += df_data["records"][i]
                if (df_data["vehicle"][i] not in aux_vehicle):
                    aux_vehicle += [df_data["vehicle"][i]]
                    df_data["vehicle_count"][v] += 1
                df_data = df_data.drop([i])
        for vehicle in aux_vehicle:
            df_data["vehicle_list"][v] = str(df_data["vehicle_list"][v]) + str(vehicle) + ' '

        df_data = df_data.reset_index(drop=True)

    df_data = df_data.reset_index(drop=True)
    total_records = df_data["records"].sum()
    df_data["total(%)"] = (df_data["records"] / total_records) * 100

    # Creating a column with Google Maps direct link to each set of coordinates for ease of analysis
    df_data["link"] = df_data.apply(lambda row: f"https://www.google.com/maps/place/{row['latitude']},{row['longitude']}", axis=1)

    df_data = df_data.drop(columns=['vehicle'])
    # Saving the results in a CSV file
    df_data.to_csv(f"{output_path}/VehicleStopsLocationFixed.csv", index=False)

