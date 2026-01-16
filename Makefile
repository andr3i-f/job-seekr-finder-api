CONTAINER_TAG = job-seekr-finder-api
DATABASE_CONTAINER_TAG = job-seekr-postgresql-dev-db

build:
	docker build -t $(CONTAINER_TAG) .

buildDb:
	docker build -t $(DATABASE_CONTAINER_TAG) -f ./postgresql_dev.dockerfile .

runDev:
	docker run -it --rm --volume .:/build --publish 8000:8000 --env-file .env $(CONTAINER_TAG)

runDb:
	docker run -d -p 5432:5432 $(DATABASE_CONTAINER_TAG)

buildRunDev:
	make build
	make runDev

buildRunDatabase:
	make buildDb
	make runDb