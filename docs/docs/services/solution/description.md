# Contest service

This service handles quiz solution checking and code solution forwarding to checkers.
Also stores the solution results.

> [OpenAPI spec](./openapi.md) 
>
> [Configuration](./config.md)

## Context

``` mermaid
flowchart
    classDef external fill:#eee,stroke:#ddd
    User["User (via ACL)"]:::external
    QuizTask["QuizTask (via ACL)"]:::external
    CodeTask["CodeTask (via ACL)"]:::external
    QuizSolution -- for a --> QuizTask
    QuizSolution -- by --> User
    CodeSolution -- for a --> CodeTask
    CodeSolution -- by --> User
    QuizChecker -- checks --> QuizSolution
```

## Stack

- Litestar
- Sqlalchemy
- Dishka
- Faststream
- Postgresql
- Minio
