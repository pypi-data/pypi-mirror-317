import requests
import pandas as pd
from typing import Optional

from energy_manager.apis.weather.get_coordinates import get_coordinates


def get_hourly_weather(
        city_name: str,
        timestamp: int,
        openweathermap_api_key: str,
) -> Optional[pd.DataFrame]:
   """
   Fetches the hourly weather data for a given city and timestamp using the OpenWeatherMap
   API and formats it into a pandas DataFrame with specific columns.

   This function retrieves historical weather data for a specific city and timestamp by making an
   API call to the OpenWeatherMap One Call Timemachine endpoint. The data is then processed into a
   DataFrame, which includes columns for datetime, temperature, and weather description. If the data
   cannot be retrieved or parsed, the function returns None.

   Args:
       city_name (str): Name of the target city for which weather data is requested.
       timestamp (int): Unix timestamp representing the date and hour for fetching weather data.
       openweathermap_api_key (str): API key for accessing the OpenWeatherMap service.

   Returns:
       Optional[pd.DataFrame]: A DataFrame containing weather data with columns for datetime,
       temperature, and weather description, or None if data cannot be retrieved or parsed.
   """
   base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine?"

   city_coordinates = get_coordinates(city_name=city_name, openweathermap_api_key=openweathermap_api_key)
   if not city_coordinates:
      print(f"Failed to retrieve coordinates for city {city_name}.")
      return None

   params = {
      "lon": city_coordinates["lon"],
      "lat": city_coordinates["lat"],
      "dt": str(timestamp),
      "appid": openweathermap_api_key,
      "units": "metric",
   }
   response = requests.get(base_url, params=params)

   if response.status_code != 200:
      print(f"Error fetching weather data: {response.status_code}")
      return None

   data = response.json()
   required_columns = ["dt", "temp", "weather"]
   hourly_weather_df = pd.DataFrame(data["data"])[required_columns]
   hourly_weather_df["dt"] = pd.to_datetime(hourly_weather_df["dt"], unit="s")
   hourly_weather_df["weather"] = hourly_weather_df["weather"].apply(lambda x: x[0]["description"])
   hourly_weather_df["temp"] = hourly_weather_df["temp"].astype(float)

   hourly_weather_df.rename(
      columns={
         "dt": "date_time",
         "temp": "temperature",
         "weather": "weather_description",
      },
      inplace=True,
   )
   return hourly_weather_df
