from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from storeapi.config import max_days_forecast, max_days_history
from storeapi.db import crudops, schemas
from storeapi.db.db_config import SessionLocal
from storeapi.models.data_fetcher import OpenWeatherApiClient
from storeapi.utils.utils import convert_celsius_to_fahrenheit

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def read_main():
    """Returns a welcome message."""
    return {"message": "Weather API"}

@router.get("/cities")
async def get_cities(db: Session = Depends(get_db)):
    """Returns supported cities."""
    cities = crudops.get_cities(db)
    
    print(f"Recieved Cities: {cities}")
    return cities


@router.get("/weather/{city}")
async def get_weather_now(city: str, db: Session = Depends(get_db)):
    """Returns current weather for a city."""
    city_req = crudops.check_city_db(db, city=city)
    # Create an instance of OpenWeatherApiClient
    client = OpenWeatherApiClient()
    weather_req = await client.get_weather(city)

    dt, main_data = weather_req["dt"], weather_req["main"]
    new_data = {
        "date": datetime.fromtimestamp(dt),
        "temp": main_data["temp"],
        "temp_fahr": convert_celsius_to_fahrenheit(main_data["temp"]),
        "owner_city": city_req.id,
    }

    return crudops.create_weather(db, schemas.WeatherIn(**new_data))

@router.get("/forecast/{city}")
async def get_weather_forecast(city: str, nextdays: int, db: Session = Depends(get_db)):
    """Returns city weather forecasts for the coming days (up to 7 days)."""
    city_req = crudops.check_city_db(db, city=city)

    if not 1 <= nextdays <= max_days_forecast:
        raise HTTPException(
            500, detail="API only returns 7 days forecast. Please request forecasts with nextdays between 1 and 7."
        )

    # Create an instance of OpenWeatherApiClient
    client = OpenWeatherApiClient()
    forecast_response = await client.get_forecast(city, nextdays)
    response_list = forecast_response["list"]

    new_data = [
        schemas.ForecastIn(
            date=date.fromtimestamp(forecast["dt"]),
            temp_day=forecast["temp"]["day"],
            temp_fahr_day=convert_celsius_to_fahrenheit(forecast["temp"]["day"]),
            owner_city=city_req.id,
        )
        for forecast in response_list
    ]

    return crudops.create_forecast(db, new_data)

@router.get("/history/{city}")
async def get_weather_history(city: str, country: str, prev: int, db: Session = Depends(get_db)):
    """Returns city weather history for the past days (up to 7 days)."""
    city_req = crudops.check_city_db(db, city=city)

    if not 1 <= prev <= max_days_history:
        raise HTTPException(
            500, detail="API only returns 7 days history. Please request history with prev between 1 and 7."
        )

    # Create an instance of OpenWeatherApiClient
    client = OpenWeatherApiClient()
    start = datetime.today() - timedelta(days=prev)
    start, end = int(start.timestamp()), int(datetime.today().timestamp())

    history_response = await client.get_history(city, country, start, end)
    history_list = history_response["list"]

    new_data = [
        schemas.HistoryIn(
            date=datetime.fromtimestamp(history["dt"]),
            temp=history["main"]["temp"],
            temp_fahr=convert_celsius_to_fahrenheit(history["main"]["temp"]),
            owner_city=city_req.id,
        )
        for history in history_list
    ]

    return crudops.create_history(db, new_data)
