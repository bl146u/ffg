FROM python:3.9.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update && apt -y upgrade

WORKDIR /opt/web

COPY ./requirements.txt .
RUN pip install --no-input -r ./requirements.txt

COPY . .
RUN chmod +x ./compose/base/gunicorn.sh ./manage.py
