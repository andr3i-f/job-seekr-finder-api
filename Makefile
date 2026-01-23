CONTAINER_TAG = job-seekr-project-api

buildProd:
	docker build -t $(CONTAINER_TAG) .

runProd:
	docker run -it --rm --publish 8000:8000 --env-file .env $(CONTAINER_TAG)

buildRunProd:
	make buildProd
	make runProd
