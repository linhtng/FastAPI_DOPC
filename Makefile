.PHONY: run pytest load-test clean re


all: run

# Run the application
run: 
	docker compose up

# Test
pytest:
	docker compose run dopc pytest -v --capture=no --verbose

load-test:
	docker compose up -d dopc
	docker compose exec dopc ./run_load_test.sh

# Stop the services
clean:
	docker rm -vf $$(docker ps -aq)
	docker rmi -f $$(docker images -aq)

re: clean all