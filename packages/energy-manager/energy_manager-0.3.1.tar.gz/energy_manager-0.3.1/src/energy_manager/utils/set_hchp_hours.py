import pandas as pd
from pathlib import Path

def set_hchp_hours():
    """
    Loads and processes the HCHP hours data from a CSV file. This function reads
    the CSV file from a specified path, converts the "hour" column to integers,
    and ensures that the "option_1", "option_2", "option_3", and "option_4"
    columns are of string type. The processed DataFrame is returned for further use.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded and processed HCHP hours
        data with the "hour" column as integers and the specified option columns
        as strings.
    """
    hchp_hours_df = pd.read_csv(filepath_or_buffer=Path(__file__).parent / "data/hchp_hours.csv")

    hchp_hours_df["hour"] =  hchp_hours_df["hour"].astype(int)
    hchp_hours_df[["option_1", "option_2", "option_3", "option_4"]] = (
        hchp_hours_df[["option_1", "option_2", "option_3", "option_4"]].astype(str))

    return hchp_hours_df
