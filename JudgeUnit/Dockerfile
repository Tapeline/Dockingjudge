FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY . .

RUN apk add curl
RUN apk add g++ gcc python3-dev musl-dev linux-headers

RUN pip install -r requirements.txt
ENV PYTHONPATH /app

CMD python judgelet/main.py
