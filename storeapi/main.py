from fastapi import FastAPI

from storeapi.db import models
from storeapi.db.db_config import engine
from storeapi.routers.weather_enpoints import router as weather_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(weather_router)
