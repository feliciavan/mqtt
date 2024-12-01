FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src/engine.py .
COPY src/webApp.py .
COPY src/testEngineOnConnect.py .
COPY src/testEngineOnMessage.py .
