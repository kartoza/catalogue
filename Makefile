export COMPOSE_FILE=deployment/docker-compose.yml
export COMPOSE_PROJECT_NAME=agritechnovation-api
export PROJECT_ID=catalogue

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:  ## Build base images
	docker-compose pull
	docker-compose build

up:  ## Bring the containers up
	docker-compose up -d devweb
