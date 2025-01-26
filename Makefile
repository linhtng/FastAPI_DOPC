.PHONY: run test clean re


all: run

# Run the application
run: 
	docker compose up

# Test
pytest:
	docker compose run dopc pytest -v --capture=no --verbose

# Stop the services
clean:
	docker rm -vf $$(docker ps -aq)
	docker rmi -f $$(docker images -aq)

re: clean all