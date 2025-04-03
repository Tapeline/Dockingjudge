FROM python:3.13.2-alpine3.21

WORKDIR /app

COPY . .

RUN apk add curl
RUN apk add g++ gcc python3-dev musl-dev linux-headers

RUN pip install poetry psutil
RUN poetry install
ENV PYTHONPATH /app

CMD chmod +x ./start.sh ; ./start.sh
