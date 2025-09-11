# Installation

To install:

1. Clone the repo:
    ```shell
    git clone https://github.com/Tapeline/Dockingjudge.git
    ```

2. Adjust the [configuration](#configuration) in `.env`

3. Prepare Judgelet:
    ```sh
    docker build -t dockingjudge-unit JudgeUnit
    ```
4. Run:
    ```shell
    docker compose up -d rabbitmq    # for some reason rabbitmq sometimes does not start properly. I am investigating this issue
    docker compose up -d --build
    ```

!!! security "Beware"

    Deployed service is expected to be put behind your main reverse proxy,
    which will handle CORS and TLS.

    Provided nginx configuration is not supplied with any security measures.

## Configuration

Configuration is done using environment variables.

!!! note
    This behaviour will be changed later to config files.

### `RMQ_USER`
> Required

RabbitMQ username

### `RMQ_PASSWORD`
> Required

RabbitMQ password

### `DB_USER`
> Required

Database username

### `DB_PASS`
> Required

Database password

### `MINIO_USER`
> Required

Minio username

### `MINIO_PASS`
> Required

Minio password

### `SECRET_KEY`
> Required

Django secret key

### `ALLOWED_HOSTS`
> Recommended

List of space-separated allowed hosts for Django.

!!! example
    `127.0.0.1 localhost dockingjudge.tapeline.dev`

### `GLOBAL_ENCODING`
> Required

Encoding to use everywhere a `.decode`/`.encode` call is needed.

!!! warning
    Not recommended to change, keep `UTF-8`.

### `COMPILERS`
> Required

List of compiler names and syntax names in following format:

```
compiler1:syntax1;compiler2;syntax2...
```

Where:

- `compiler` is a name of a compiler in judge system.
- `syntax` is a name of a syntax that will be used in highlightinh


### `ALLOW_CONTEST_CREATION_TO`
> Optional, default = `*`

List of usernames to allow contest creation to, separated by `;`.

Set to `*` to allow contest creation to all users.
