FROM python:3.10.13

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY requirements-dev.txt /app/requirements-dev.txt

RUN pip install -r requirements.txt 
RUN pip install -r requirements-dev.txt 



COPY . /app