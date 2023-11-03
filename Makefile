include ./.env

build:
	docker build -t real-estate-previsor --no-cache .

run:
	docker run --env-file .env --network ${DEV_CONTAINER_NETWORK} -p 80:80 --name real-estate-previsor -d real-estate-previsor
