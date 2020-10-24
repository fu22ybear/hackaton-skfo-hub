wd:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

network:=hackaton-skfo-hub_internal

producer:=python-producer
consumer:=python-consumer
oscillogram_analyzer:=python-oscillogram-analyzer


# compose
compose-build:
	docker-compose build

compose-run: compose-rm compose-build
	docker-compose up

compose-run-d: compose-rm compose-build
	docker-compose up -d

compose-stop:
	- docker stop zookeeper kafka clickhouse grafana metabase minio

compose-rm: compose-stop
	- docker rm zookeeper kafka clickhouse grafana metabase minio


# producer
producer-build:
	docker build \
		-f ./docker/${producer}/Dockerfile \
		-t ${producer} \
		./docker/${producer}/

producer-run: producer-stop
	docker run -ti --rm \
		--name ${producer} \
		--env-file ${wd}/docker/${producer}/.env \
		--volume ${wd}/docker/${producer}/:/app \
		--network ${network} \
		--link kafka:kafka \
		${producer}

producer-run-d: producer-stop producer-build
	docker run -ti -d --rm \
		--name ${producer} \
		--env-file ${wd}/docker/${producer}/.env \
		--volume ${wd}/docker/${producer}/:/app \
		--network ${network} \
		--link kafka:kafka \
		${producer}

producer-stop:
	- docker stop ${producer}

producer-rename-oscillograms:
	bash ./docker/${producer}/rename_produced_oscillograms.sh

# consumer
consumer-build:
	docker build \
		-f ./docker/${consumer}/Dockerfile \
		-t ${consumer} \
		./docker/${consumer}/

consumer-run: consumer-stop
	docker run -ti --rm \
		--name ${consumer} \
		--env-file ${wd}/docker/${consumer}/.env \
		--volume ${wd}/docker/${consumer}/:/app \
		--network ${network} \
		--link kafka:kafka \
		--link clickhouse:clickhouse \
		--link minio:minio \
		${consumer}

consumer-run-d: consumer-stop consumer-build
	docker run -ti -d --rm \
		--name ${consumer} \
		--env-file ${wd}/docker/${consumer}/.env \
		--volume ${wd}/docker/${consumer}/:/app \
		--network ${network} \
		--link kafka:kafka \
		--link minio:minio \
		${consumer}

consumer-stop:
	- docker stop ${consumer}

# oscillogram_analyzer
oscillogram_analyzer-build:
	docker build \
		-f ./docker/${oscillogram_analyzer}/Dockerfile \
		-t ${oscillogram_analyzer} \
		./docker/${oscillogram_analyzer}/

oscillogram_analyzer-run: oscillogram_analyzer-stop
	docker run -ti --rm \
		--name ${oscillogram_analyzer} \
		--env-file ${wd}/docker/${oscillogram_analyzer}/.env \
		--volume ${wd}/docker/${oscillogram_analyzer}/:/app \
		--network ${network} \
		--link kafka:kafka \
		--link clickhouse:clickhouse \
		--link minio:minio \
		${oscillogram_analyzer}

oscillogram_analyzer-run-d: oscillogram_analyzer-stop oscillogram_analyzer-build
	docker run -ti -d --rm \
		--name ${oscillogram_analyzer} \
		--env-file ${wd}/docker/${oscillogram_analyzer}/.env \
		--volume ${wd}/docker/${oscillogram_analyzer}/:/app \
		--network ${network} \
		--link kafka:kafka \
		--link minio:minio \
		${oscillogram_analyzer}

oscillogram_analyzer-stop:
	- docker stop ${oscillogram_analyzer}


# all
all-stop:
	- docker stop zookeeper kafka clickhouse grafana metabase minio ${producer} ${consumer}

all-rm: all-stop
	- docker rm zookeeper kafka clickhouse grafana metabase minio ${producer} ${consumer}
