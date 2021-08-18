FROM python:3.8-slim-buster
WORKDIR /strativ
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py migrate