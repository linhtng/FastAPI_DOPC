.PHONY: run test clean re

# Create directories for mounting volumes

all: run

# Run the application
run: 
	docker compose up

# Test
test:
	docker compose run DOPC pytest

# Stop the services
clean:
	docker rm -vf $$(docker ps -aq)
	docker rmi -f $$(docker images -aq)

re: clean all