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

- [ ] More security on judgelet
    - [x] run judgelet as non-root
    - [ ] run solutions as different users
    - [ ] utilize chown and chmod to protect non-solution files
    - [ ] (maybe) introduce bubblewrap
- [x] Add more compilers (at least cpp)
- [ ] deploy from ghcr.io
- [ ] Add tests
    - [x] judgelet
    - [ ] judge svc
    - [x] solution svc
    - [x] contest svc
    - [x] account svc
    - [ ] e2e
- [ ] Lint and test in CI
    - [x] judgelet
    - [ ] judge svc
    - [x] solution svc
    - [x] contest svc
    - [x] account svc
    - [ ] e2e
- [x] Move config to config files
    - [x] judgelet
    - [x] solution svc
    - [x] contest svc
    - [x] account svc
- [ ] Add struct logging
    - [x] solution svc
    - [ ] contest svc
    - [ ] account svc
    - [ ] judge svc
- [x] Add metrics
    - [x] contest svc
    - [x] account svc
- [ ] tidy up in docker-compose.yml

### Second round

- [ ] Make frontend locally deployable in container
- [ ] Massive frontend rework
- [ ] Add contest timer
- [ ] Add profile pictures
- [ ] Get rid of pydantic in application layer (bruh)

### Third round

- [ ] Migrate from RMQ to NATS
- [ ] Add tracing
    - [ ] judge svc
    - [ ] solution svc
    - [ ] contest svc
    - [ ] account svc
- [ ] Load testing

### Fourth round

- [ ] Add messages
- [ ] add DL (disk limit) verdict
      returned when sandbox occupies too much disk space
- [ ] Public/private contests

### Bugs

- [x] registration 400 "a server error occurred". Add more informative error message.
- [x] standings are messed up

### Docs

- [ ] Describe each service separately
    - [ ] judgelet
    - [ ] judge svc
    - [ ] solution svc
    - [ ] contest svc
    - [ ] account svc
- [ ] Add openapi to docs
