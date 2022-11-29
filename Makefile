build:
	docker build -t gnpsclassicalgroups . 

bash:
	docker run -it --rm gnpsclassicalgroups /bin/bash

server-compose-build-nocache:
	docker-compose --compatibility build --no-cache

server-compose-interactive:
	docker-compose --compatibility build
	docker-compose --compatibility up

server-compose:
	docker-compose --compatibility build
	docker-compose --compatibility up -d

server-compose-production:
	docker-compose --compatibility build
	docker-compose --compatibility up -d

attach:
	docker exec -i -t gnpsclassicalgroups-dash /bin/bash
