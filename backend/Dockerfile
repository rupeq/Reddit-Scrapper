FROM python:3.8.5

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./src /code/

ENV DISPLAY=:99

RUN pip install -r requirements.txt