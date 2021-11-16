export COMPOSE_FILE=deployment/docker-compose.yml
export COMPOSE_PROJECT_NAME=catalogue
export PROJECT_ID=catalogue
OPTS :=

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: pull build up db-restore migrate ## first setup

deploy:  ## Build and push the to the private repo
	docker-compose build uwsgi
	docker tag catalogue_uwsgi:latest cr.kartoza.com/sansa_catalogue
	docker push cr.kartoza.com/sansa_catalogue

pull:  ## Pull pre-built images
	docker-compose pull

build:  ## Build base images
	docker-compose build

db_up:
	docker-compose up -d db
	docker-compose run check_db

up: db_up  ## Bring the containers up
	docker-compose up -d devweb

production_up: db_up
	docker-compose up -d web

down:  ## Bring down the containers
	docker-compose down

run:  ## Run Django Server
	docker-compose exec devweb python manage.py runserver --verbosity 3 0.0.0.0:8080

restart: down up

clean:  ## Cleanup local docker files for this project
	docker-compose down --rmi all -v
	-sudo rm -rf deployment/backups deployment/data deployment/logs deployment/media deployment/pg deployment/reports deployment/static

shell:  ## Get into the django shell
	docker-compose exec devweb bash

pyshell:  ## Get into the django python shell
	docker-compose exec devweb python manage.py shell

migrate:  ## Run migrations
	docker-compose exec devweb python manage.py migrate

makemigrations:  ## Create migrations
	docker-compose exec devweb python manage.py makemigrations

test:  ## Run test cases
	docker-compose exec devweb python manage.py test $(OPTS)

db-backup:  ## Create a database backup
	docker-compose exec db su - postgres -c "pg_dumpall" | gzip -9 > latest.sql.gz

db-restore:  ## Restore a database backup
	gzip -cd latest.sql.gz | docker exec -i $(PROJECT_ID)-db bash -c 'PGPASSWORD=docker psql -U docker -h localhost postgres'

db-shell:
	docker-compose exec db bash

django-test:
	@docker-compose exec devweb python manage.py test --noinput --verbosity 3 catalogue
