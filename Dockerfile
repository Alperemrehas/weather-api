FROM python:3.10.13

WORKDIR /app
COPY requirments.txt /app/requirements.txt
COPY requirments-dev.txt /app/requirements-dev.txt

RUN pip install -r requirements.txt 
RUN pip install -r requirements-dev.txt 



COPY . /app