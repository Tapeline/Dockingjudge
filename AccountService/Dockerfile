ARG build_variant=full

FROM python:3.12-alpine3.21 AS base

WORKDIR /app

RUN apk add uv git
COPY . .
RUN chmod +x ./start.sh

FROM base AS sync_full
RUN uv sync --all-groups

FROM base AS sync_min
RUN uv sync

FROM sync_${build_variant} AS final

CMD ./start.sh
