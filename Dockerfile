FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=MovieProject.settings
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

RUN mkdir -p staticfiles

RUN python manage.py tailwind install

RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput

CMD gunicorn MovieProject.wsgi:application --bind 0.0.0.0:$PORT