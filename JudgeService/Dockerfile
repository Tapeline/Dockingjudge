FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY . .
RUN chmod +x ./start.sh

RUN pip install poetry
ENV PYTHONPATH /app
RUN poetry install

CMD ./start.sh
