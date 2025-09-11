# Dockingjudge stack

Dockingjudge is built on top of following technologies.

## Account service

- Django, DRF
- uvicorn
- PostgreSQL

## Contest service

- Django, DRF
- uvicorn
- PostgreSQL

## Judge service

- Faststream (rabbitmq)
- dishka

## Judgelet

- Litestar
- dishka

## Solution service

- Litestar
- Faststream (rabbitmq)
- dishka
- PostgreSQL
- minio

## Monitoring

- Grafana
- Loki
- Prometheus
- Promtail
- cAdvisor
- nodeexporter
