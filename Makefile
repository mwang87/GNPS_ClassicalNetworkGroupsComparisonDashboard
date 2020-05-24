build:
	docker build -t gnpsclassicalgroups . 

bash:
	docker run -it --rm gnpsclassicalgroups /bin/bash

server-compose-build-nocache:
	docker-compose build --no-cache

server-compose-interactive:
	docker-compose build
	docker-compose up

server-compose:
	docker-compose build
	docker-compose up -d

attach:
	docker exec -i -t gnpsclassicalgroups-dash /bin/bash
