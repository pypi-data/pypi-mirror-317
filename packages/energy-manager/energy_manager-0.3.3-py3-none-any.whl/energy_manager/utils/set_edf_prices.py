import pandas as pd


def set_edf_prices():
    """
    Creates and returns a DataFrame containing EDF subscription plans and their
    corresponding electricity prices for both normal and peak hours.

    The DataFrame is structured with the following columns:
    1. `subscription`: Names of the subscription plans.
    2. `kwh_price_normal_hour`: Price per kWh during normal hours for each plan.
    3. `kwh_price_peak_hour`: Price per kWh during peak hours for each plan.

    Returns:
        pd.DataFrame: A DataFrame object with EDF subscription plans and their
        electricity prices.
    """
    edf_prices_df = pd.DataFrame(
        {
            "subscription": ["Base", "Heures Creuses - Heures Pleines"],
            "kwh_price_normal_hour": [25.16, 20.68],
            "kwh_price_peak_hour": [25.16, 27.00]
        }
    )
    return edf_prices_df
