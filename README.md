# Dockingjudge

**⚠ WIP, MVP**

---

<!-- TOC -->
* [Dockingjudge](#dockingjudge)
  * [Demo](#demo)
  * [Deployment](#deployment)
    * [Dev env](#dev-env)
  * [Structure](#structure)
  * [Planned](#planned)
    * [First round](#first-round)
    * [Second round](#second-round)
    * [Third round](#third-round)
    * [Bugs](#bugs)
<!-- TOC -->

---

## Demo

[View full demo](https://docs.dockingjudge.tapeline.dev/explore/demo)

![](docs/docs/img/ui-code-task.png)

![](docs/docs/img/ui-markdown-page.png)

[View full demo](https://docs.dockingjudge.tapeline.dev/explore/demo)

## Deployment
(you may want to replace the domain name in files with you own)

```sh
docker build -t dockingjudge-unit JudgeUnit
docker compose up -d rabbitmq    # for some reason rabbitmq sometimes does not start properly. I am investigating this issue
docker compose up -d --build
```

also replace example sensitive information in .env (like SECRET_KEY).

You can consult [docs](https://docs.dockingjudge.tapeline.dev/admin/install) for more info.

### Dev env
If you want to deploy locally, without a domain, then you
need to deploy frontend separately:
1. ```sh
   $ cd Frontend
   $ npm install --legacy-peer-deps
   $ npm run dev -- --host --port 3000
   ```
2. ```nginx configuration
   # api_gateway_nginx.conf
   
   # proxy_pass http://frontend.service:3000;
   proxy_pass http://host.docker.internal:3000;
   ```

## Structure

Dockingjudge consists of several services:

![](docs/docs/arch/containers.png)

(formalised arch definition located in [dockingjudge.aisle](dockingjudge.aisle))


## Planned

### First round

- [x] More security on judgelet
- [x] Add more compilers (at least cpp)
- [ ] Migrate from RMQ to NATS/Kafka
- [ ] deploy from ghcr.io
- [ ] Add tests
    - [x] judgelet
    - [ ] judge svc
    - [ ] solution svc
    - [ ] contest svc
    - [ ] account svc
    - [ ] e2e
- [ ] Lint and test in CI
    - [x] judgelet
    - [ ] judge svc
    - [ ] solution svc
    - [ ] contest svc
    - [ ] account svc
    - [ ] e2e
- [ ] Move config to config files
    - [x] judgelet
    - [ ] solution svc
    - [ ] contest svc
    - [ ] account svc
- [ ] Add tracing
    - [ ] solution svc
    - [ ] contest svc
    - [ ] account svc

### Second round

- [ ] Load testing
- [ ] Make frontend locally deployable in container
- [ ] Massive frontend rework
- [ ] Get rid of pydantic in application layer (bruh)

### Third round

- [ ] Add contest timer
- [ ] Add messages
- [ ] Add profile pictures
- [ ] add DL (disk limit) verdict
      returned when sandbox occupies too much disk space
- [ ] Public/private contests

### Bugs

- [ ] registration 400 "a server error occurred". Add more informative error message.
- [ ] standings are messed up

### Docs

- [ ] Describe each service separately
    - [ ] judgelet
    - [ ] judge svc
    - [ ] solution svc
    - [ ] contest svc
    - [ ] account svc
- [ ] Add openapi to docs
