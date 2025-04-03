```sh
docker plugin install grafana/loki-docker-driver:3.2.1 --alias loki --grant-all-permissions
docker build -t dockingjudge-unit JudgeUnit
docker compose up -d
```
