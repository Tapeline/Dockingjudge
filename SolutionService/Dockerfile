FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY . .
RUN chmod +x ./start.sh

RUN pip3 install poetry
RUN poetry install

CMD chmod +x ./start.sh ; ./start.sh
