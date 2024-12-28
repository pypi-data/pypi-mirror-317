import requests
from unidecode import unidecode
from typing import Dict, Optional


def get_coordinates(
        city_name: str,
        openweathermap_api_key: str,
) -> Optional[Dict[str, float]]:
    """
    Fetches geographical coordinates (latitude and longitude) for a given city name
    using the OpenWeatherMap API. This function restricts the search to cities located
    in France and returns the coordinates only if the city is found in France.

    Args:
        city_name: The name of the city for which to fetch the geographical coordinates.
        openweathermap_api_key: The API key to authenticate with the OpenWeatherMap API.

    Returns:
        Optional[Dict[str, float]]: A dictionary with the keys 'lat' and 'lon' that
        represent the latitude and longitude of the city, respectively. Returns None
        if the city is not found, if it is not located in France, or if there is an
        error in the API request.
    """
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{unidecode(city_name.strip().lower())}",
        "limit": 1,
        "appid": openweathermap_api_key,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:

        data = response.json()
        country_code = data[0]["country"] if data else None

        if not country_code:
            print(f"Country code not found for city {city_name}.")
            return None

        if country_code == "FR":
            city_coordinates = {"lat": data[0]["lat"], "lon": data[0]["lon"]}
            return city_coordinates

        print(f"City {city_name} not found in France. Please, specify a city known in France.")
        return None

    print(f"Error fetching data: {response.status_code}")
    return None
