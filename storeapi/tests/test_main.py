from fastapi.testclient import TestClient

from storeapi.main import app

# Create a TestClient instance to interact with the FastAPI application
client = TestClient(app)

def test_get_cities_returns_200():
    """
    Test the /cities endpoint to ensure it returns a 200 status code.
    """
    response = client.get("/cities")
    assert response.status_code == 200

def test_get_weather_today_returns_200():
    """
    Test the /weather/{city} endpoint to ensure it returns a 200 status code.
    """
    response = client.get("/weather/Istanbul")
    assert response.status_code == 200

def test_forecast_returns_200():
    """
    Test the /forecast/{city} endpoint to ensure it returns a 200 status code.
    """
    response = client.get("/forecast/London?nextdays=4")
    assert response.status_code == 200

def test_history_returns_200():
    """
    Test the /history/{city} endpoint to ensure it returns a 200 status code.
    """
    response = client.get("/history/Istanbul?country=tr&prev=3")
    assert response.status_code == 200

def test_forecast_max_days_fail_returns_500():
    """
    Test the /forecast/{city} endpoint with invalid nextdays to ensure it returns a 500 status code.
    """
    response = client.get("/forecast/London?nextdays=10")
    assert response.status_code == 500

def test_weather_city_fail_returns_500():
    """
    Test the /weather/{city} endpoint with an unsupported city to ensure it returns a 500 status code.
    """
    response = client.get("/weather/kayseriya")
    assert response.status_code == 404
