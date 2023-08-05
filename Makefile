up:
	sudo docker-compose -f docker-compose.yaml up --build -d
show-logs:
	sudo docker-compose -f docker-compose.yaml logs -f api
down:
	sudo docker-compose -f docker-compose.yaml down

start-test:
	sudo docker-compose -f docker-compose-test.yaml up --build -d
show-result:
	sudo docker-compose -f docker-compose-test.yaml logs -f test_api
drop-test:
	sudo docker-compose -f docker-compose-test.yaml down
