import pandas as pd
from typing import List, Optional

from energy_manager.apis.weather.get_coordinates import get_coordinates
from energy_manager.apis.weather.get_hourly_weather import get_hourly_weather


def get_daily_weather(
        city_name: str,
        openweathermap_api_key: str,
        timestamps: List[int],
) -> Optional[pd.DataFrame]:
   """
   Fetch daily weather data for a given city from OpenWeatherMap API over specified timestamps.

   This function retrieves hourly weather data for each provided timestamp, concatenates
   the data into a single DataFrame, and returns the resulting DataFrame. If the city
   coordinates cannot be fetched or any timestamp fails to provide weather data, the
   function returns None.

   Args:
       city_name (str): The name of the city for which weather data is to be fetched.
       openweathermap_api_key (str): The API key for authenticating with the OpenWeatherMap API.
       timestamps (List[int]): Unix timestamp values for which hourly weather data should
           be fetched.

   Returns:
       Optional[pd.DataFrame]: A pandas DataFrame containing the concatenated weather data
       for all specified timestamps, or None if an error occurs.
   """
   if not get_coordinates(
           city_name=city_name,
           openweathermap_api_key=openweathermap_api_key
   ):
      print(f"Failed to fetch city coordinates for city name {city_name}.")
      return None

   daily_weather_df = []
   for timestamp in timestamps:
      hourly_weather_df = get_hourly_weather(
         city_name=city_name,
         openweathermap_api_key=openweathermap_api_key,
         timestamp=timestamp
      )
      if hourly_weather_df is None:
         print(f"Failed to fetch weather data for timestamp {timestamp}.")
         return None
      daily_weather_df.append(hourly_weather_df)

   daily_weather_df = pd.concat(daily_weather_df, ignore_index=True)
   return daily_weather_df
