FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /djangoProject

COPY . .
RUN pip install -r requirements.txt

