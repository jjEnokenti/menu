up:
	sudo docker-compose -f docker-compose.yaml up --build
down:
	sudo docker-compose -f docker-compose.yaml down

starttest:
	sudo docker-compose -f docker-compose-test.yaml up --build
droptest:
	sudo docker-compose -f docker-compose-test.yaml down
