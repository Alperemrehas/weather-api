# Weather-API

Welcome to the Weather-API repository This API provides information about current weather, forecasts, and historical weather data for supported cities using the OpenWeatherMap API.

## Getting Started
Before running the application with docker, make sure you have the docker installed on your host and the engine is started.

-[Docker](https://www.docker.com/products/docker-desktop/) 

In order to get service, you need to have API_KEY, so you can have the API with the help of this document:

- [API_KEY](https://openweathermap.org/appid)

### Installation and Running

#### Runing The File(Without Docker)

1. Clone the repository:
        '''
        git clone https://github.com/Alperemrehas/weather-api.git
        cd weather-api
        '''
2. Please make ready the API_KEY and create a .env file it the weather_api directory and add your API_KEYs. You can get help from .env.example file.

3. Now you need to install the requriments, in order to do this we recomend to use a virtual env.(eg.: pyhton -m venv .venv)
        '''
        pip install -r requirments.txt
        pip install -r requirments-dev.txt
        '''
4. If everything installed succesfully than you could run the app by typing: 

        uvicorn storeapi.main:app --reload --host 0.0.0.0 --port 2525 

5. You can check the interactive API document, by hiting:
    
    http://127.0.0.1:8000/docs 

#### Runing The File(With Docker)

1. Clone the repository:

        '''
        git clone https://github.com/Alperemrehas/weather-api.git \
        cd weather-api \
        '''

2. Please make ready the API_KEY and create a .env file it the weather_api directory and add your API_KEYs. You can get help from .env.example file.
        '''
        docker compose up 
        '''

3. Endpoints

        http://localhost:2525/cities 
        http://localhost:2525/weather/Ankara 
        http://localhost:2525/forecast/London?nextdays=4 
        http://localhost:2525/history/Ankara?country=TR&prev=1 

4. In order to run the test, during the time app is up and running you have to open a new terminal and run the code:
         '''
        docker exec -it weather-api-web python -m pytest -v
        '''