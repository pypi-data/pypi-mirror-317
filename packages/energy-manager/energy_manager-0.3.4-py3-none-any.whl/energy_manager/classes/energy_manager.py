import pandas as pd

from energy_manager.expenses.compute_daily_expenses import compute_daily_expenses


class EnergyManager(object):
    """
    Manages energy consumption and calculates expenses based on provided parameters.

    This class is designed to handle energy management by leveraging data like
    city name, average energy usage, temperature, and insulation factor. It interacts
    with external APIs to compute daily energy expenses, taking into consideration
    climatic and usage factors.

    Attributes:
        _city_name (str): The name of the city for which energy expenses are calculated.
        _dpe_usage (float): The average energy usage (DPE - Diagnostic de Performance
            Énergétique) of the property in kWh/m².year.
        _temperature (float): The current temperature in the city, used for expense calculations.
        _openweathermap_api_key (str): API key for accessing OpenWeatherMap's forecast data.
        _insulation_factor (float): Adjustment factor accounting for the property's insulation
            efficiency. Defaults to 1.0, corresponding to standard insulation.
    """

    def __init__(
            self,
            city_name: str,
            dpe_usage: float,
            temperature: float,
            openweathermap_api_key: str,
            insulation_factor: float = 1.0,
    ):
        if not isinstance(city_name, str) or city_name.strip() == "":
            raise ValueError("city_name must be a non-empty string")
        if dpe_usage <= 0:
            raise ValueError("dpe_usage must be a positive number")
        if insulation_factor <= 0:
            raise ValueError("insulation_factor must be greater than 0")
        self._city_name = city_name
        self._dpe_usage = dpe_usage
        self._temperature = temperature
        self._openweathermap_api_key = openweathermap_api_key
        self._insulation_factor = insulation_factor

    def get_daily_expenses(self) -> pd.DataFrame:
        daily_expenses_df = compute_daily_expenses(
            city_name=self._city_name,
            openweathermap_api_key=self._openweathermap_api_key,
            temperature=self._temperature,
            dpe_usage=self._dpe_usage,
            insulation_factor=self._insulation_factor,
        )
        return daily_expenses_df
