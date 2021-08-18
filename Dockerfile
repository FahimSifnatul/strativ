FROM python:3.8-slim-buster
WORKDIR /strativ
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput