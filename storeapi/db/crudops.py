from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from storeapi.config import TIME_TO_UPDATE_CURRENT_WEATHER

from . import models, schemas


def create_city(db: Session, city_name: str):
    """
    Create a new city in the database.

    Args:
        db (Session): Database session.
        city_name (str): Name of the city to be created.

    Returns:
        models.City: Created city object.
    """
    db_city = models.City(name=city_name)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    """
    Get a list of supported cities from the database.

    Args:
        db (Session): Database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to retrieve.

    Returns:
        list: List of supported cities.
    """
    return db.query(models.City).offset(skip).limit(limit).all()


def check_city_db(db: Session, city: str):
    """
    Check if a city exists in the database.

    Args:
        db (Session): Database session.
        city_name (str): Name of the city to check.

    Returns:
        models.City: City object if it exists.

    Raises:
        HTTPException: If the city is not found.
    """
    cities = db.query(models.City).filter(models.City.name == city).first()
    if not cities:
        cities=create_city(db, city)
        #raise HTTPException(status_code=404, detail="City not found")
    return cities


def create_weather(db: Session, weather: schemas.WeatherIn):
    """
    Create weather entry in the database.

    Args:
        db (Session): Database session.
        weather (schemas.WeatherIn): Weather data to be stored.

    Returns:
        models.Weather: Created weather object.
    """
    db_weather = models.Weather(**weather.model_dump())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


def get_weather_today(db: Session, city: schemas.City, current_time: datetime):
    """
    Get the latest weather entry for a city.

    Args:
        db (Session): Database session.
        city (schemas.City): City object.
        current_time (datetime): Current time.

    Returns:
        models.Weather: Latest weather entry for the city.
    """
    prev_hour = current_time - timedelta(minutes=TIME_TO_UPDATE_CURRENT_WEATHER)
    return db.query(models.Weather).filter(
        models.Weather.date > prev_hour,
        models.Weather.owner_city == city.id
    ).first()


def check_forecast_db(db: Session, city: schemas.City, next_days: int, current_date: datetime):
    """
    Check if forecast data exists in the database.

    Args:
        db (Session): Database session.
        city (schemas.City): City object.
        next_days (int): Number of days for forecast.
        current_date (datetime): Current date.

    Returns:
        list: List of forecast entries.
    """
    max_date = current_date + timedelta(next_days - 1)
    return db.query(models.Forecast).filter(
        models.Forecast.date.between(current_date, max_date),
        models.Forecast.owner_city == city.id
    ).all()


def create_forecast(db: Session, forecasts: schemas.ForecastIn):
    """
    Create forecast entries in the database.

    Args:
        db (Session): Database session.
        forecasts (schemas.ForecastIn): Forecast data to be stored.

    Returns:
        list: List of created forecast objects.
    """
    for forecast in forecasts:
        db_forecast = models.Forecast(**forecast.model_dump())
        record = db.query(models.Forecast).filter(
            models.Forecast.date == db_forecast.date,
            models.Forecast.owner_city == db_forecast.owner_city
        ).first()
        if not record:
            db.add(db_forecast)
    db.commit()
    return forecasts


def check_history_db(db: Session, city: schemas.City, prev_days: int, current_date: datetime):
    """
    Check if historical data exists in the database.

    Args:
        db (Session): Database session.
        city (schemas.City): City object.
        prev_days (int): Number of previous days for history.
        current_date (datetime): Current date.

    Returns:
        list: List of historical entries.
    """
    min_date = current_date - timedelta(prev_days)
    return db.query(models.History).filter(
        models.History.date.between(min_date, current_date),
        models.History.owner_city == city.id
    ).all()


def create_history(db: Session, history_data: schemas.HistoryIn):
    """
    Create historical entries in the database.

    Args:
        db (Session): Database session.
        history_data (schemas.HistoryIn): Historical data to be stored.

    Returns:
        list: List of created historical objects.
    """
    for history in history_data:
        db_history = models.History(**history.model_dump())
        record = db.query(models.History).filter(
            models.History.date == db_history.date,
            models.History.owner_city == db_history.owner_city
        ).first()
        if not record:
            db.add(db_history)
    db.commit()
    return history_data
