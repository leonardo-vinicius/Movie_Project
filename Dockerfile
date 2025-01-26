FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py tailwind build

CMD gunicorn MovieProject.wsgi:application --bind 0.0.0.0:$PORT