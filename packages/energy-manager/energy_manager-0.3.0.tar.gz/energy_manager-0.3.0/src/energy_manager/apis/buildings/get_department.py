import requests
from typing import Optional
from unidecode import unidecode


def get_department(city_name: str) -> Optional[str]:
    """
    Fetches the department name of a given city in France through a public API.

    This function uses the OpenDataSoft API to retrieve the department name corresponding
    to the provided city name. It fetches, cleans, and parameterizes the query before making
    a GET request to the API endpoint. If a department name is found for the given city,
    it is returned; otherwise, None is returned. The function also handles and logs errors
    or unsuccessful API responses.

    Args:
        city_name: The name of the city for which the department name is to be retrieved.
            The input will be normalized by removing diacritics, converting to lowercase,
            and stripping leading/trailing spaces.

    Returns:
        Optional[str]: The name of the department corresponding to the provided city,
            or None if no department is found or an API error occurs.
    """
    base_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-france-commune/records"
    params = {
        "select": "com_name_lower,dep_name",
        "where": f"com_name_lower = '{unidecode(city_name.strip().lower())}'",
        "limit": 1,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["results"]:
            department_name = data["results"][0]["dep_name"][0]
            return department_name

        print(f"No department found for city {city_name}.")
        return None

    print(f"Error fetching data: {response.status_code}")
    return None
