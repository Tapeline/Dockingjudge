FROM python:3.13.2-alpine3.21

WORKDIR /app

COPY . .

RUN apk add curl
RUN apk add uv
RUN apk add g++ gcc python3-dev musl-dev linux-headers

RUN uv sync

CMD chmod +x ./start.sh ; ./start.sh
