# Dockingjudge repo structure

## `.github`

Contains GitHub-related stuff. 

- `workflows`

    Defines CI workflows that run for Dockingjudge repo. 
    Pull requests regarding this directory require extended review.

- `issue_templates`

    Defines handy templates for different issue types, so users
    can send their report as quickly as possible.


## Service sources

> - `AccountService`
> - `ContestService`
> - `JudgeService`
> - `JudgeUnit`
> - `SolutionService`

Contain source code for main services.

### Source code

One or two packages with service sources (may be wrapped in `src`). 

Examples:
- `src`
- `api`
- `something_service`

### Bootstrapping files

Files for startup, e.g.:

- `manage.py` (for Django)
- `start.sh`

### Tests

`tests` directory with unit tests.

### Quality control configs

- `.coveragerc`
- `.flake8`
- `mypy.ini`
- `ruff.toml`

!!! note
    Changes in these files require prior discussion with the maintainer.

### Tooling configs

- `docker-compose-something.yml`
- `Dockerfile`
- `justfile`
- `pyproject.toml`
- `uv.lock`

!!! note
    Changes in these files require prior discussion with the maintainer.

### Service configs

- `something_config.yml`

Contain per-service settings. They are also used as a base in Compose deployment.


## Documentation sources

Located in `docs`.

- `docs`

    Actual MD sources.

- `*.aisle`

    C4 diagram sources (generated files **are** tracked by Git)

- `docs/arch`
    
    C4 diagram generation results

- `docs/openapi`

    Generated OpenAPI specs (generated files **are** tracked by Git)

- `justfile`

    Helper commands for building docs

- `macros.py`

    Custom macros this documentation uses

- `mkdocs.yml`

    Docs config

- `pyproject.toml`, `uv.lock`

    Project settings


## `Frontend`

SPA frontend sources are located here.

## `Infrastructure`

Contains various services configs and Docker Compose manifests
to assemble the whole project.

!!! note
    Changes in these files require prior discussion with the maintainer.

## `Tests`

System, E2E, UI tests.

