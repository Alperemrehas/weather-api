import os

import httpx
from dotenv import load_dotenv
from fastapi.exceptions import HTTPException
from httpx import Response

from storeapi.config import units

# load environment variables from .env file

load_dotenv()

class OpenWeatherApiClient:
    def __init__(self):
        # Load API keys and set base URLs
        self.api_key = os.getenv("API_KEY")
        self.api_key_history = os.getenv("API_KEY_HISTORY")
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.history_url = "https://history.openweathermap.org/data/2.5/"

    async def _make_request(self, endpoint: str, params: dict):
        """
        Make an asynchronous HTTP request to the OpenWeatherMap API.

        Args:
            endpoint (str): The API endpoint to append to the base URL.
            params (dict): Parameters to include in the request.

        Returns:
            dict: JSON response from the API.

        Raises:
            HTTPException: If the response status code is not 200.
        """

        
        print("Executing _make_request method")
        url = f"{self.base_url}{endpoint}"
        print(f"Request URL: {url}")

        async with httpx.AsyncClient() as client:
            if endpoint =="history/city":
                response: Response = await client.get(f"{self.history_url}{endpoint}", params=params)
            else:
                response: Response = await client.get(f"{self.base_url}{endpoint}", params=params)
            if response.status_code != 200:
                raise HTTPException(response.status_code, detail=response.text)
            return response.json()

    async def get_weather(self, city: str):
        """
        Get current weather data for a specific city.

        Args:
            city (str): The name of the city.

        Returns:
            dict: Current weather data for the specified city.
        """
        params = {"q": city, "appid": self.api_key, "units": units}
        return await self._make_request("weather", params)

    async def get_history(self, city: str, country: str, start: str, end: str):
        """
        Get historical weather data for a specific city within a date range.

        Args:
            city (str): The name of the city.
            country (str): The country code.
            start (str): The start date of the historical data.
            end (str): The end date of the historical data.

        Returns:
            dict: Historical weather data for the specified city and date range.
        """
        params = {
            "q": f"{city},{country}",
            "type": "hour",
            "appid": self.api_key_history,
            "units": units,
            "start": start,
            "end": end,
            "cnt": 1,
        }
        return await self._make_request("history/city", params)

    async def get_forecast(self, city: str, cnt: int):
        """
        Get weather forecast for a specific city.

        Args:
            city (str): The name of the city.
            cnt (int): The number of days for the forecast.

        Returns:
            dict: Weather forecast for the specified city.
        """
        params = {"q": city, "appid": self.api_key, "units": units, "cnt": cnt}
        return await self._make_request("forecast/daily", params)

# Example usage:
async def example_usage():
    client = OpenWeatherApiClient()
    weather_data = await client.get_weather("London")
    history_data = await client.get_history("London", "GB", "start_time", "end_time")
    forecast_data = await client.get_forecast("London", 5)
    print(weather_data, history_data, forecast_data)

# You can now create an instance of OpenWeatherApiClient and use its methods for making API requests.
