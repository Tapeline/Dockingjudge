# Contest service

This service handles contest and task management, user participation and timer.

> [OpenAPI spec](./openapi.md) 
>
> [Configuration](./config.md)

## Context

``` mermaid
flowchart
    classDef external fill:#eee,stroke:#ddd
    User["User (via ACL)"]:::external
    Contest
    ContestSession
    TextPage -- belongs to --> Contest
    QuizTask -- belongs to --> Contest
    CodeTask -- belongs to --> Contest
    ContestSession -- issued by --> Contest
    ContestSession -- belongs to --> User
```

## Stack

- Django 
- DRF
- Postgresql
