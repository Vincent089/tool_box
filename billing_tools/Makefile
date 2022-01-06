build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

reload: down build up

prod-image:
	docker build -f ./docker/prod/Dockerfile -t vincecgi89/billing-tools .

publish-prod-image: prod-image
	docker push vincecgi89/billing-tools