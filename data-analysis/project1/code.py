from sqlalchemy.orm import joinedload
from database import session, Deal
import pandas as pd
import json
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import matplotlib.pyplot as plt
from database import fetch_by_identification
import requests
import os

WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')

"""
Goal: Cross the temperature of different battery components with the ambient temperature.

Used external API for the ambient temperature:
Documentation: https://weather.com/swagger-docs/ui/sun/v1/sunV1Site-BasedObservationHistorical.json

    location_temp - temperature of the location where the vehicle is driving
    obs_name - name of the observatory providing local temperature
    rh - relative humidity, always expressed as a percentage
    heat_index - apparent tempeture due to warm temperatures and high humidity
    pressure - barometric pressure
    wdir - magnetic direction from which the wind blows, expressed in degrees (where 0 indicates wind from the north, 90 from the east, 180 from the south, and 270 from the west)
    gust - wind gust speed
    precip_hrly - precipitation for the previous hour
    precip_total - precipitation for the previous day, for a rolling period of 24 hours
    snow_hrly - snow accumulation for the previous hour
"""

def aggregate(group):
    """
    Aggregate temperature data from a group.

    Parameters:
        group (pandas.DataFrame): A DataFrame containing vehicle data.

    Returns:
        pandas.DataFrame: Aggregated vehicle data.
    """

    agg = {
        'imei': group.imei.iloc[0],
        'time': group.time.iloc[0],
        'latitude': group.latitude.iloc[0],
        'longitude': group.longitude.iloc[0],
        'battery_max_t': group.battery_max_t.max(),
        'battery_max_t (median)': group.battery_max_t.median(),
        'battery_min_t': group.battery_min_t.min(),
        'battery_min_t (median)': group.battery_min_t.median(),
        'lc_temp (max)': group.lc_temp.max(),
        'lc_temp (min)': group.lc_temp.min(),
        'lc_temp (median)': group.lc_temp.median(),
        'lc_xmc_temp (max)': group.lc_xmc_temp.max(),
        'lc_xmc_temp (min)': group.lc_xmc_temp.min(),
        'lc_xmc_temp (median)': group.lc_xmc_temp.median(),
        'lc_power_supply_temp (max)': group.lc_power_supply_temp.max(),
        'lc_power_supply_temp (min)': group.lc_power_supply_temp.min(),
        'lc_power_supply_temp (median)': group.lc_power_supply_temp.median(),
        'lc_igbt1_temp (max)': group.lc_igbt1_temp.max(),
        'lc_igbt1_temp (min)': group.lc_igbt1_temp.min(),
        'lc_igbt1_temp (median)': group.lc_igbt1_temp.median(),
        'lc_igbt2_temp (max)': group.lc_igbt2_temp.max(),
        'lc_igbt2_temp (min)': group.lc_igbt2_temp.min(),
        'lc_igbt2_temp (median)': group.lc_igbt2_temp.median(),
        'mc_temp (max)': group.mc_temp.max(),
        'mc_temp (min)': group.mc_temp.min(),
        'mc_temp (median)': group.mc_temp.median(),
        'mc_xmc_temp (max)': group.mc_xmc_temp.max(),
        'mc_xmc_temp (min)': group.mc_xmc_temp.min(),
        'mc_xmc_temp (median)': group.mc_xmc_temp.median(),
        'mc_power_supply_temp (max)': group.mc_power_supply_temp.max(),
        'mc_power_supply_temp (min)': group.mc_power_supply_temp.min(),
        'mc_power_supply_temp (median)': group.mc_power_supply_temp.median(),
        'mc_igbt_temp (max)': group.mc_igbt_temp.max(),
        'mc_igbt_temp (min)': group.mc_igbt_temp.min(),
        'mc_igbt_temp (median)': group.mc_igbt_temp.median(),
        'mc_motor_temp (max)': group.mc_motor_temp.max(),
        'mc_motor_temp (min)': group.mc_motor_temp.min(),
        'mc_motor_temp (median)': group.mc_motor_temp.median(),
        'dci_temp (max)': group.dci_temp.max(),
        'dci_temp (min)': group.dci_temp.min(),
        'dci_temp (median)': group.dci_temp.median(),
        'mlu_temp (max)': group.mlu_temp.max(),
        'mlu_temp (min)': group.mlu_temp.min(),
        'mlu_temp (median)': group.mlu_temp.median(),
        'fibo_choke_temp (max)': group.fibo_choke_temp.max(),
        'fibo_choke_temp (min)': group.fibo_choke_temp.min(),
        'fibo_choke_temp (median)': group.fibo_choke_temp.median(),
        'fibo_pcb_temp (max)': group.fibo_pcb_temp.max(),
        'fibo_pcb_temp (min)': group.fibo_pcb_temp.min(),
        'fibo_pcb_temp (median)': group.fibo_pcb_temp.median()
    }
    return pd.DataFrame(agg, index=[0])

def read_vehicle_data(df, resample_period):
    """
    Read and aggregate vehicle data.

    Parameters:
        df (pandas.DataFrame): DataFrame containing raw vehicle data.
        resample_period (str): The resample period for aggregating data.

    Returns:
        pandas.DataFrame: Aggregated vehicle data.
    """

    df["registered_at"] = pd.to_datetime(df["registered_at"])
    df.rename(columns={"motor_controller_temperature": "mc_temp", "motor_controller_xmc_temperature": "mc_xmc_temp", 
                       "motor_controller_power_supply_temperature": "mc_power_supply_temp", "motor_controller_igbt_temperature": "mc_igbt_temp",
                       "motor_controller_motor_temperature": "mc_motor_temp", "dci_temperature": "dci_temp", "mlu_temperature": "mlu_temp", 
                       "load_controller_igbt_temperature_2": "lc_igbt2_temp","load_controller_igbt_temperature_1": "lc_igbt1_temp", 
                       "load_controller_power_supply_temperature" :"lc_power_supply_temp", "load_controller_xmc_temperature": "lc_xmc_temp", 
                       "load_controller_temperature": "lc_temp", "battery_min_temperature": "battery_min_t", "battery_max_temperature": "battery_max_t", 
                       "registered_at": "time", "mlu_temperature": "mlu_temp", "fibo_choke_temperature": "fibo_choke_temp", 
                       "fibo_pcb_temperature": "fibo_pcb_temp"}, inplace = True)
    # using aggregate to fetch min, max and median data, resampled by variable "resample_period"
    grouped = df.groupby(pd.Grouper(freq = str(resample_period), key='time'))
    try:
        df = grouped.apply(aggregate)
        return df
    except:
        return 

def read_temp_data(df):
    """
    Read and clean temperature data from an external API.

    Parameters:
        df (pandas.DataFrame): DataFrame containing vehicle data.

    Returns:
        pandas.DataFrame: Cleaned temperature data.
    """

    df.reset_index(inplace=True, drop = True)
    # getting all unique days in the fetched data
    unique_days = df["time"].dt.date.unique()
    df["date"] = df["time"].dt.date
    latitude = []
    longitude = []
    # fetching latitude and longitude for each unique day (in order to get location temperature)
    for day in unique_days:
        coords = df.loc[df["date"] == day]
        latitude += [coords["latitude"].iloc[0]]
        longitude += [coords["longitude"].iloc[0]]

    # preparing, fetching and cleaning the data from the weather API
    df_aid = pd.DataFrame()
    for i in range(0, len(unique_days) - 1):
        start = unique_days[i]
        end = unique_days[i + 1]
        start = start.strftime("%Y%m%d")
        end = end.strftime("%Y%m%d")
        url = f'https://api.weather.com/v1/geocode/{latitude[i]}/{longitude[i]}/observations/historical.json'
        print(f'requesting temp on {latitude[i]}, {longitude[i]}')
        r = requests.get(f"""{url}?apiKey={WEATHER_API_KEY}&units=m&startDate={start}&endDate={end}""")
        data = json.loads(r.text)
        try:
            df_aid = pd.concat([df_aid, pd.DataFrame(data["observations"])])
        except:
            break   
    df_aid["valid_time_gmt"] = pd.to_datetime(df_aid['valid_time_gmt'], unit='s')
    df_aid["valid_time_gmt_hour"] = df_aid['valid_time_gmt'].astype('string').str.slice(0,13)
    df_aid = df_aid[["temp", "valid_time_gmt_hour", "obs_name", "rh", "heat_index", "pressure", "wdir", "gust", "precip_hrly", "precip_total", "snow_hrly"]]
    df_aid = df_aid.drop_duplicates('valid_time_gmt_hour', keep='first')
    return df_aid

def plot_battery_t(df, imei):
    """
    Plot battery temperatures over time.

    Parameters:
        df (pandas.DataFrame): DataFrame containing battery temperature data.
        imei (str): IMEI number of the vehicle.

    Returns:
        None
    """

    df['hour'] = pd.to_datetime(df['hour'])
    plt.figure(figsize=(20,5))
    plt.title("Imei " + str(imei) + " Battery Temperatures")
    plt.plot(df["hour"], df["battery_max_t"], label='battery_max_temperature (max)')
    plt.plot(df["hour"], df["battery_min_t"], label='battery_min_temperature (min)')
    plt.plot(df["hour"], df["location_temp"], label='location_temperature')
    plt.ylabel("Temperature")
    plt.xlabel("Time")
    plt.legend(loc='best')
    df = df.reset_index(drop=True)
    df['time'] = pd.to_datetime(df['hour'])
    aux = df["hour"][0]
    
    # changing the color of the plot's background for better visualization (using 1 month interval)
    while aux <= df["hour"][len(df) - 1] - relativedelta(months = 1):
        temp = aux
        aux += relativedelta(months = 1)
        plt.axvspan(temp, aux, facecolor='0.6', alpha=0.5)
        aux += relativedelta(months = 1) 
    if (aux < df["hour"][len(df) - 1]):
        plt.axvspan(aux, df["time"][len(df) - 1], facecolor='0.6', alpha=0.5)

def plot_controller_t(df, imei, controller):
    """
    Plot controller temperatures over time.

    Parameters:
        df (pandas.DataFrame): DataFrame containing controller temperature data.
        imei (str): IMEI number of the vehicle.
        controller (str): Name of the controller.

    Returns:
        None
    """

    df['hour'] = pd.to_datetime(df['hour'])
    plt.figure(figsize=(20,5))
    plt.title(f"IMEI {str(imei)} {controller} Temperatures")
    plt.plot(df["hour"], df[f"{controller}_temp (max)"], label=f'{controller}_temp (max)')
    plt.plot(df["hour"], df[f"{controller}_temp (min)"], label=f'{controller}_temp (min)')
    plt.plot(df["hour"], df["location_temp"], label='location_temperature')
    plt.ylabel("Temperature")
    plt.xlabel("Time")
    plt.legend(loc='best')
    df = df.reset_index(drop=True)
    df['time'] = pd.to_datetime(df['hour'])
    aux = df["time"][0]

    # changing the color of the plot's background for better visualization (using 1 month interval)
    while aux <= df["time"][len(df) - 1] - relativedelta(months = 1):
        temp = aux
        aux += relativedelta(months = 1)
        plt.axvspan(temp, aux, facecolor='0.6', alpha=0.5)
        aux += relativedelta(months = 1) 
    if (aux < df["hour"][len(df) - 1]):
        plt.axvspan(aux, df["time"][len(df) - 1], facecolor='0.6', alpha=0.5)

def proj_1 (imei, resample_period, timestamp_start, timestamp_end, output_path='/temp'):
    """
    Perform temperature analysis and visualization for a vehicle.

    Parameters:
        imei (str): IMEI number of the vehicle.
        resample_period (str): The resample period for aggregating data.
        timestamp_start (datetime): Start timestamp for data fetching.
        timestamp_end (datetime): End timestamp for data fetching.
        output_path (str, optional): Output path for saving visualizations.

    Returns:
        None
    """

    df_all = pd.DataFrame()

    # Parameters for fetching data
    columns = ["imei", "registered_at", "battery_min_temperature", "battery_max_temperature", "load_controller_temperature", "load_controller_xmc_temperature", "load_controller_power_supply_temperature", "load_controller_igbt_temperature_1", "load_controller_igbt_temperature_2", "motor_controller_temperature", "motor_controller_xmc_temperature", "motor_controller_power_supply_temperature", "motor_controller_igbt_temperature", "motor_controller_motor_temperature", "dci_temperature", "mlu_temperature", "latitude", "longitude", "mlu_temperature", "fibo_choke_temperature", "fibo_pcb_temperature"]

    # Fetching raw data, 5 days each time (from "timestamp_start" until "timestamp_end")
    timestamp_aux = timestamp_start + timedelta(days=5)
    while (timestamp_aux != (timestamp_end + timedelta(days=5))):
        timestamp_begin = timestamp_aux - timedelta(days=5)
        if (timestamp_aux >= timestamp_end):
            timestamp_aux = timestamp_end
        df = fetch_by_identification(imei, timestamp_begin, timestamp_aux, columns)
        df = read_vehicle_data(df, resample_period)
        timestamp_aux += timedelta(days=5)
        try:
            df_all = pd.concat([df_all, df])
        except:
            break

    df = df_all

    if df.empty:
        print('no data found in the interval. skipping...')
        return 

    # Select only first 13 chars of data which are what we'll use to compare.
    df["hour"] = df["time"].astype('string').str.slice(0, 13)

    # Also selecting only day, in order to iterate through time later
    df["day"] = df["time"].astype('string').str.slice(0, 10)

    # Read historical temperature data and joining the ambient data with the vehicle data
    df_aid = read_temp_data(df)
    df = df.set_index('hour').join(df_aid.set_index('valid_time_gmt_hour'))
    df.reset_index(inplace = True)
    df = df.rename(columns={'index': 'hour', 'temp': 'location_temp'})

    df.drop(df.loc[df['latitude'] == 0].index, inplace = True)
    df.to_csv(f"{output_path}/vehicle_temperature.csv", index=False)

    df["time"] = df["time"].dt.tz_localize(None)

    # Plot and save graphs with "resample_period" intervals between values
    plot_battery_t(df, imei)
    plt.savefig(f"{output_path}/"f"{resample_period}_battery_temperatures.png")

    for controller in ['lc_igbt1', 'lc_igbt2', 'dci']:
        plot_controller_t(df, imei, controller)
        plt.savefig(f"{output_path}/"f"{resample_period}_{controller}_temperatures.png")
