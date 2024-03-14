FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./src/
COPY ./src /src
WORKDIR /src
EXPOSE 8000


RUN pip install -r requirements.txt

