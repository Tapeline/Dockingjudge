FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY . .

RUN apk --no-cache add curl
RUN apk add g++

RUN pip install -r requirements.txt
ENV PYTHONPATH /app

CMD python judgelet/main.py
