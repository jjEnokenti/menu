up:
	sudo docker-compose -f docker-compose.yaml up --build -d --force-recreate
show-logs:
	sudo docker-compose -f docker-compose.yaml logs -f api
down:
	sudo docker-compose -f docker-compose.yaml down
postman-test:
	sudo docker-compose -f docker-compose.yaml down
	sudo docker-compose -f docker-compose.yaml up --build -d db cache api

start-test:
	sudo docker-compose -f docker-compose-test.yaml up --build -d
show-result:
	sudo docker-compose -f docker-compose-test.yaml logs -f test_api
drop-test:
	sudo docker-compose -f docker-compose-test.yaml down
