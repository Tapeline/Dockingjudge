ARG build_variant

FROM python:3.13.2-alpine3.21 AS base

WORKDIR /app

RUN apk add curl
RUN apk add uv
RUN apk add g++ gcc python3-dev musl-dev linux-headers
RUN apk add git

COPY . .

RUN adduser -D limited && chown -R limited /app
USER limited

FROM base AS sync_full
RUN uv sync --all-groups

FROM base AS sync_min
RUN uv sync

FROM sync_${build_variant} AS final
CMD chmod +x ./start.sh ; ./start.sh
