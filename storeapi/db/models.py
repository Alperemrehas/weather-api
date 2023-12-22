from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db_config import Base


class City(Base):
    """
    Database model for storing information about cities.
    """
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Establishing a bidirectional relationship with the Weather model
    weathers = relationship("Weather", back_populates="city", lazy="dynamic")

class Weather(Base):
    """
    Database model for storing weather information.
    """
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    temp = Column(Float)
    temp_fahr = Column(Float)

    # Establishing a bidirectional relationship with the City model
    owner_city = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", back_populates="weathers")

class Forecast(Base):
    """
    Database model for storing weather forecast information.
    """
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    temp_day = Column(Float)
    temp_fahr_day = Column(Float)

    # Establishing a bidirectional relationship with the City model
    owner_city = Column(Integer, ForeignKey("cities.id"))

class History(Base):
    """
    Database model for storing weather history information.
    """
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    temp = Column(Float)
    temp_fahr = Column(Float)

    # Establishing a bidirectional relationship with the City model
    owner_city = Column(Integer, ForeignKey("cities.id"))
