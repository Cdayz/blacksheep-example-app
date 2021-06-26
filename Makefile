.PHONY: requiements
requiements:
	poetry export -f requirements.txt > requirements.txt

.PHONY: up
up: requiements
	docker-compose -f docker-compose.yml --project-name features up --build

.PHONY: cleanup
cleanup:
	docker-compose -f docker-compose.yml --project-name features down -v --remove-orphans
