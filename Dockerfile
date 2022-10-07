FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN apt update && apt install gettext-base && pip install -r requirements.txt
COPY . .