COMPOSE_FILE:=./compose/docker-compose.yml


# Installation

install:
	pip install --no-cache-dir --no-input --requirement ./requirements.txt

uninstall:
	pip uninstall -y -r <(pip freeze)

reinstall: uninstall install


# Docker compose

up:
	docker-compose -f $(COMPOSE_FILE) up

build:
	docker-compose -f $(COMPOSE_FILE) build

build_nocache:
	docker-compose -f $(COMPOSE_FILE) build --no-cache

create:
	docker-compose -f $(COMPOSE_FILE) create

start:
	docker-compose -f $(COMPOSE_FILE) start

restart:
	docker-compose -f $(COMPOSE_FILE) restart

stop:
	docker-compose -f $(COMPOSE_FILE) stop

remove: stop
	docker-compose -f $(COMPOSE_FILE) rm -f

ps:
	docker-compose -f $(COMPOSE_FILE) ps

images:
	docker-compose -f $(COMPOSE_FILE) images


# Docker

logs:
	docker logs -f --tail=1000 $(c)

exec:
	docker exec -it $(c) /bin/bash

clear_system:
	docker system prune -f

clear_builder:
	docker builder prune -f


# Django admin

app:
	django-admin startapp $(a)


# Django manage

run:
	./manage.py runserver

migrate:
	./manage.py migrate

migrations:
	./manage.py makemigrations

superuser:
	./manage.py createsuperuser

shell:
	./manage.py shell

collectstatic:
	./manage.py collectstatic --noinput

compress:
	./manage.py compress -v 0

locale_make:
	./manage.py makemessages -a

locale_compile:
	./manage.py compilemessages


# Build and run

containers_restart: remove build create start
