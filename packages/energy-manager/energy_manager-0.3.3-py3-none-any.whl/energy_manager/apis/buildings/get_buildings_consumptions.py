import requests
import pandas as pd
from typing import Optional

from energy_manager.utils.set_dpe_mappings import set_dpe_mappings
from energy_manager.apis.buildings.get_department import get_department

DPE_CATEGORIES = ["A", "B", "C", "D", "E", "F"]


def get_buildings_consumptions(city_name: str) -> Optional[pd.DataFrame]:
    """
    Fetches and processes energy consumption data of buildings for a given city.

    This function retrieves energy consumption data of residential buildings from an
    open dataset API based on the provided city name. It filters the data for buildings
    constructed from the year 2000 onwards, ensures energy classification data exists,
    and includes only certain types of buildings such as apartments, houses, or collective
    housing. It renames and processes the resulting data to calculate energy consumption
    in kilowatt-hours per square meter using predefined mappings.

    Args:
        city_name (str): The name of the city for which to fetch and analyze energy
            consumption data.

    Returns:
        Optional[pd.DataFrame]: A pandas DataFrame containing the filtered and processed
            building energy consumption data. The DataFrame has the following columns:
            - dpe_class: The energy performance class of the building.
            - building_type: The type of the building (e.g., Apartment, House).
            - consumption_in_kwh_per_square_meter: The energy consumption of the building
              in kilowatt-hours per square meter.
            Returns None if no data is available or if an error occurs during the
            fetching process.

    Raises:
        KeyError: Raised if the response data structure differs unexpectedly.
        ValueError: Raised if the API response data cannot be processed due to unexpected
            content or format inconsistencies.
    """
    base_url = ("https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
                "base-des-diagnostics-de-performance-energetique-dpe-des-batiments-residentiels-p/records")
    department_name = get_department(city_name=city_name)

    if department_name:

        params = {
            "select": "classe_energie,"
                      " tr002_type_batiment_id",
            "where": f"annee_construction is not null and "
                     f"annee_construction >= date'2000' and "
                     f"classe_energie is not null and "
                     f"surface_habitable is not null and "
                     f"(tr002_type_batiment_id = \"Appartement\" or "
                     f"tr002_type_batiment_id = \"Maison\" or "
                     f"tr002_type_batiment_id = \"Logements collectifs\") and "
                     f"nom_dep = \"{department_name}\" and "
                     f"(classe_energie = \"A\" or "
                     f"classe_energie = \"B\" or "
                     f"classe_energie = \"C\" or "
                     f"classe_energie = \"D\" or "
                     f"classe_energie = \"E\" or "
                     f"classe_energie = \"F\")",
            "group_by": "classe_energie, tr002_type_batiment_id",
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            if data["results"]:
                data_df = pd.DataFrame(data["results"])

                data_df.rename(
                    columns={
                        "classe_energie": "dpe_class",
                        "tr002_type_batiment_id": "building_type",
                    },
                    inplace=True
                )
                data_df["building_type"] = data_df["building_type"].astype(str)
                data_df["dpe_class"] = pd.Categorical(
                    data_df["dpe_class"],
                    categories=DPE_CATEGORIES,
                    ordered=True,
                )

                data_df["consumption_in_kwh_per_square_meter"] = data_df["dpe_class"].apply(
                    lambda x: set_dpe_mappings().get(x, None)).astype(float) / (365*24)

                return data_df

            print(f"No info on buildings energy consumption found for the city {city_name}.")
            return None

        print(f"Error fetching data: {response.status_code}")
        return None

    print(f"No department found for city {city_name}.")
    return None
