uv run python manage.py migrate
uv run python manage.py rmq_init &
uv run python manage.py rmq_worker &
uv run uvicorn contest_service.asgi:application --host 0.0.0.0 --port 8000
wait
