# event_management_task

## How to run:

```bash
docker compose up --build
docker compose run django-web python manage.py makemigrations
docker compose run django-web python manage.py migrate

Swagger documentation :
http://localhost:8000/swagger/
