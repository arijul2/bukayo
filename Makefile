dev-up:
	docker-compose -f docker-compose-dev.yml --env-file ./.env.dev up --build

.PHONY: dev-up
