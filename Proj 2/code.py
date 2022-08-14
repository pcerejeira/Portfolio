import pandas as pd
import numpy as np
from database import fetch_deal_summary
from datetime import timedelta
from database.query import fetch_deal_from_licensee, fetch_vehicle_operation_1min

"""
Goal: Fetching all stops (non facilities) from given vehicles/deals (fetching deals by each Addvolt's licensee)
"""

def proj_2 (timestamp_start, timestamp_end, output_path='/temp'):
    deals = fetch_deal_from_licensee(licensee)
    df_final = pd.DataFrame(columns=['fk_deal', 'registered_at', 'latitude', 'longitude', 'is_in_facilities', 'vehicle_is_stopped'])
    
    # Fetching 15 days each time from database table "vehicle_operation_1min"
    for deal in deals:
        timestamp_aux = timestamp_start + timedelta(days=15)
        while (timestamp_aux != (timestamp_end + timedelta(days=15))):
            timestamp_begin = timestamp_aux - timedelta(days=15)
            if (timestamp_aux >= timestamp_end):
                timestamp_aux = timestamp_end
            df = fetch_vehicle_operation_1min(deal, timestamp_begin, timestamp_aux)
            df_final = pd.concat([df_final, df])
            timestamp_aux += timedelta(days=15)
    
    df_final = df_final.drop(columns=['registered_at', 'vehicle_is_stopped'])
    df_final = df_final.round({'latitude': 3, 'longitude': 3})

    # Grouping stops by each fk_deal and respective coordinates, saving number of occurrences
    df_final = df_final.groupby(['fk_deal', 'latitude', 'longitude']).count()
    df_final.rename(columns = {'is_in_facilities':'records'}, inplace = True)

    # Cleaning data, dropping non significant stops and default/error values
    df_data = df_final
    df_data = df_data.reset_index(drop = False)
    df_data = df_data[df_data.records > 50]
    df_data = df_data[df_data.latitude != 0]
    df_data = df_data[df_data.longitude != 0]

    df_data["deal_count"] = 1
    df_data["deals"] = ""

    # Considering each nearby coordinate as the same, using 0.003 in this case, based on https://en.wikipedia.org/wiki/Decimal_degrees
    # Grouping all stops by latitude and longitude, saving the number of occurrences as "records" and each related vehicle ID in "deals"
    df_data = df_data.reset_index(drop = True)
    for v in range(0, len(df_data) - 1):
        if v > len(df_data) - 1:
            break
        aux_deal = [df_data["fk_deal"][v]]
        for i in range(v + 1, len(df_data) - 1):
            if (df_data["latitude"][v] - 0.003 <= df_data["latitude"][i] <= df_data["latitude"][v] + 0.003 and df_data["longitude"][v] -0.003 <= df_data["longitude"][i] <= df_data["longitude"][v] + 0.003):
                df_data["records"][v] += df_data["records"][i]
                if (df_data["fk_deal"][i] not in aux_deal):
                    aux_deal += [df_data["fk_deal"][i]]
                    df_data["deal_count"][v] += 1
                df_data = df_data.drop([i])
        for i in aux_deal:
            df_data["deals"][v] = str(df_data["deals"][v]) + str(i) + ' '

        df_data = df_data.reset_index(drop = True)

    df_data = df_data.reset_index(drop = True)
    df_data["total(%)"] = df_data["records"].sum()
    # Creating a column with google maps direct link to each coordinates, for ease of analysis
    df_data["link"] = np.NaN
    for i in range (0, len(df_data)):
        df_data["total(%)"][i] = (df_data["records"][i] / df_data["total(%)"][i]) * 100
        df_data["link"][i] = "https://www.google.com/maps/place/" + str(df_data['latitude'][i]) + "," + str(df_data['longitude'][i])

    df_data = df_data.drop(columns=['fk_deal'])
    # Saving the results in a CSV file
    df_data.to_csv(f"{output_path}/DealsStopsLocationFixed.csv", index=False)
