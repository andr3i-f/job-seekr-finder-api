CONTAINER_TAG = job-seekr-finder-api

build:
	docker build -t $(CONTAINER_TAG) .

runDev:
	docker run -it --rm --volume .:/app --publish 8000:8000 --env-file .env $(CONTAINER_TAG)

buildRunDev:
	make build
	make runDev