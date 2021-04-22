export COMPOSE_FILE=deployment/docker-compose.yml
export COMPOSE_PROJECT_NAME=catalogue
export PROJECT_ID=catalogue
OPTS :=

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: build up ## first setup

build:  ## Build base images
	docker-compose pull
	docker-compose build

up:  ## Bring the containers up
	docker-compose up -d db
	docker-compose run check_db
	docker-compose up -d devweb

down:  ## Bring down the containers
	docker-compose down

clean:  ## Cleanup local docker files for this project
	docker-compose down --rmi all -v

shell:  ## Get into the django shell
	docker-compose exec devweb bash

pyshell:  ## Get into the django python shell
	docker-compose exec devweb python manage.py shell

test:
	docker-compose exec devweb python manage.py test $(OPTS)

db-backup:  ## Create a database backup
	docker-compose exec db su - postgres -c "pg_dumpall" | gzip -9 > latest.sql.gz

db-restore:  ## Restore a database backup
	gzip -cd latest.sql.gz | docker exec -i $(PROJECT_ID)-db bash -c 'PGPASSWORD=docker psql -U docker -h localhost postgres'
