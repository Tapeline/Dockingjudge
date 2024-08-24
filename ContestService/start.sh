python manage.py makemigrations
python manage.py migrate
python manage.py rmq_init &
python manage.py rmq_worker &
uvicorn contest_service.asgi:application --host 0.0.0.0 --port 8000
wait
