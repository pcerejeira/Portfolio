from sqlalchemy.orm import joinedload
from database import session, Deal
import pandas as pd
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt


def concat(df, dados):
    # Renaming columns for ease coding and coherence. Removing missing values.
    for data in dados:
        temp = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + "/data/" + data)
        temp.rename(columns={"battery_min_temperature": "min_t", "battery_max_temperature": "max_t", "registered_at": "time"}, inplace = True)  # TODO: porque é preciso?
        temp.dropna(subset = ["min_t"], inplace=True)
        df = pd.concat([df, temp])
    return df

def read_vehicle_data(df):
    df["time"] = pd.to_datetime(df["time"])
    df = df.resample('10min', on="time").max()
    df.dropna(subset = ["min_t"], inplace=True)
    # df.reset_index(inplace=True)
    return df

def read_temp_data(df, temperaturas):
    df_lisbon = pd.DataFrame()
    for temp in temperaturas:
        data = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/temperature/" + temp))
        df_aid = pd.DataFrame(data["observations"])
        df_lisbon = pd.concat([df_lisbon, df_aid])
    df_lisbon.reset_index(drop=True, inplace=True)
    df_lisbon["valid_time_gmt"] = pd.to_datetime(df_lisbon['valid_time_gmt'], unit='s')
    df_lisbon["valid_time_gmt_hour"] = df_lisbon['valid_time_gmt'].astype('string').str.slice(0,13)

    # Select only relevant columns out of temperature data.
    df_comparing = pd.DataFrame()
    df_comparing["time"] = df_lisbon["valid_time_gmt"]
    df_comparing["hour"] = df_lisbon["valid_time_gmt_hour"]
    df_comparing["temp"] = df_lisbon["temp"]
    return df_comparing

def plot_battery_t(df_final):
    plt.figure(figsize=(20,5))
    plt.title("Battery Temperatures")
    plt.plot(df_final["time_right"], df_final["min_t"], label='battery_min_temperature')
    plt.plot(df_final["time_right"], df_final["max_t"], label='battery_max_temperature')
    plt.plot(df_final["time_right"], df_final["temp"], label='lisbon_t')
    plt.ylabel("Temperature")
    plt.xlabel("Time")
    plt.legend(loc='best')

def plot_controller_t(df_final):
    plt.figure(figsize=(20,5))
    plt.title("Controller Temperatures")
    plt.plot(df_final["time_right"], df_final["load_controller_igbt_temperature_1"], label='controller_1')
    plt.plot(df_final["time_right"], df_final["load_controller_igbt_temperature_2"], label='controller_2')
    #plt.plot(df_final["time_right"], df_final["motor_controller_igbt_temperature"], label='motor_controller')
    plt.plot(df_final["time_right"], df_final["temp"], label='lisbon_t')
    plt.ylabel("Temperature")
    plt.xlabel("Time")
    plt.legend(loc='best')

def problem10(output_path='/temp'):
    dados = os.listdir("analysis/problem10/data")
    temperaturas = os.listdir("analysis/problem10/temperature")

    # Load data from all files in `dados` to df.
    df = pd.DataFrame()
    df = concat(df, dados)

    # Resample vehicle data to 10 min intervals.
    df = read_vehicle_data(df)

    # Select only first 13 chars of data which are what we'll use to compare.
    df["hour"] = df["time"].astype('string').str.slice(0, 13)

    # Read historical temperature data
    df_comparing = read_temp_data(df, temperaturas)

    # Merge raw data with temperature data
    df_final = df.set_index('hour').join(df_comparing.set_index('hour'),how = 'left', lsuffix='_left', rsuffix='_right')
    df_final.reset_index(inplace=True)
    df_final.to_csv("temp/vehicle_temperature.csv")

    df_final.drop(df_final[df_final.min_t < -10].index, inplace=True)

    # Plot and save graphs with 10 mins and 1 day interval between values
    plot_battery_t(df_final)
    plt.savefig("temp/10mins_battery_temperatures.png")
    plt.show()

    plot_controller_t(df_final)
    plt.savefig("temp/10mins_controller_temperatures.png")
    plt.show()

    df_final = df_final.resample('1D', on="time_right").max()

    plot_battery_t(df_final)
    plt.savefig("temp/daily_battery_temperatures.png")
    plt.show()

    plot_controller_t(df_final)
    plt.savefig("temp/daily_controller_temperatures.png")
    plt.show()