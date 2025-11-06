# Account service

This service handles user storage and authorization.

> [OpenAPI spec](./openapi.md) 
>
> [Configuration](./config.md)

## Context

``` mermaid
flowchart
    User 
    AccessToken
    AccessToken -- belongs to --> User
```

## Stack

- Django 
- DRF
- Postgresql
