# Cross-platform shell configuration
# Use PowerShell on Windows (higher precedence than shell setting)
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
# Use sh on Unix-like systems
set shell := ["sh", "-c"]


up *PARAMS:
    docker compose -f Infrastructure/docker-compose.yml up -d {{PARAMS}}

up-ci *PARAMS:
    docker compose -f Infrastructure/docker-compose.yml -f Infrastructure/docker-compose-ci.yml up -d {{PARAMS}}

down *PARAMS:
    docker compose -f Infrastructure/docker-compose.yml down {{PARAMS}}

stop *PARAMS:
    docker compose -f Infrastructure/docker-compose.yml stop {{PARAMS}}

compose *PARAMS:
    docker compose -f Infrastructure/docker-compose.yml {{PARAMS}}
