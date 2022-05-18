FROM "python:3.7"

RUN mkdir /binance_bot

WORKDIR /binance_bot

COPY ./binance_bot /binance_bot

COPY requirements.txt /binance_bot/

RUN pip install -r requirements.txt

ADD . /binance_bot/