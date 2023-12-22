FROM python:3.10.13

WORKDIR /app
COPY requirments.txt /app/requirments.txt
COPY requirments-dev.txt /app/requirments-dev.txt

RUN pip install -r requirments.txt 
RUN pip install -r requirments-dev.txt 



COPY . /app