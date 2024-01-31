import pandas as pd
from database import fetch_deal_summary
from datetime import timedelta
from database.query import fetch_by_imei
import time

"""
Goal: Fetching high generator current variations for given deals, every 4 seconds >= 20
"""


def proj_3(imei, timestamp_start, timestamp_end, output_path="/temp"):
    df_final = pd.DataFrame(columns=["registered_at", "sum_current_diff"])
    # Selecting desired columns
    columns = ["imei", "registered_at", "motor_controller_current_ac"]

    occurences = 0
    result_dict = {}

    start = time.time()
    print("Started at time: ", start)

    # Fetching raw_data 5 days each time
    timestamp_aux = timestamp_start + timedelta(days=5)
    while timestamp_aux != (timestamp_end + timedelta(days=5)):
        should_remove = False

        timestamp_begin = timestamp_aux - timedelta(days=5)
        if timestamp_aux >= timestamp_end:
            timestamp_aux = timestamp_end
        df = fetch_by_imei(imei, timestamp_begin, timestamp_aux, columns)
        timestamp_aux += timedelta(days=5)

        # Compute the absolute difference between consecutive rows
        df["generator_current_diff"] = (
            df["motor_controller_current_ac"].diff().abs().iloc[1:]
        )

        df["registered_at"] = pd.to_datetime(df["registered_at"])
        # Convert to datetime object
        try:
            df["id"] = (
                df.index // 2
            )  # Add a new column for grouping every 2 rows, we are grouping every 2 rows and checking the sum with the one right before, so we don't skip any value
        except:
            continue

        df_grouped = (
            df.groupby("id")
            .agg({"generator_current_diff": "sum", "registered_at": "first"})
            .reset_index()
        )
        df_grouped["sum_current_diff"] = df_grouped[
            "generator_current_diff"
        ] + df_grouped["generator_current_diff"].shift(1)
        filtered_df = df_grouped[
            (df_grouped["generator_current_diff"] >= 20)
            | (df_grouped["sum_current_diff"] >= 20)
        ]

        # Initialize a list to store the row indices to be removed
        rows_to_remove = []

        # Iterate over the DataFrame rows
        for index, row in filtered_df.iterrows():
            current_id = row["id"]
            current_diff = row["generator_current_diff"]

            if should_remove:
                should_remove = False
                continue

            # Check if generator_current_diff >= 20
            if current_diff >= 20:
                # Check if there exists a row with ID equal to current_id + 1 (identify duplicated values)
                next_row = filtered_df[filtered_df["id"] == current_id + 1]
                if not next_row.empty:
                    # Add the row index to the list of rows to be removed
                    rows_to_remove.append(index)
                    should_remove = True

        # Remove the identified rows from the DataFrame, this rows are repetitions, inheriting the variation in current from the previous ones
        filtered_df.drop(rows_to_remove, inplace=True)

        # Select desired columns
        filtered_df = filtered_df[["registered_at", "sum_current_diff"]]

        df_final = pd.concat([df_final, filtered_df], ignore_index=True)

        occurences += len(filtered_df)

        # Iterate over the rows
        for _, row in filtered_df.iterrows():
            sum_diff = row["sum_current_diff"]

            # Determine the range label based on sum_diff
            if sum_diff >= 20 and sum_diff < 25:
                label = "20-25"
            elif sum_diff >= 25 and sum_diff < 30:
                label = "25-30"
            elif sum_diff >= 30 and sum_diff < 35:
                label = "30-35"
            elif sum_diff >= 35 and sum_diff < 40:
                label = "35-40"
            else:
                label = "40+"

            # Update the count in the dictionary
            result_dict[label] = result_dict.get(label, 0) + 1

    # Saving results
    df_final.to_csv(f"{output_path}/GeneratorCurrentVariations.csv", index=False)

    end = time.time()
    print(end - start)

    print("There were ", occurences, "occurences")
    print("The distribution was ", result_dict)
    return occurences

