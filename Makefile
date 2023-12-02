replication_factor ?= 1
partitions ?= 1
ingestion_interval ?= 3


build:
	docker-compose build
up:
	docker-compose up
down:
	docker-compose down
cleanup:
	docker-compose down --remove-orphans -v
create-topic:
	docker-compose exec kafka1 kafka-topics --create --zookeeper zookeeper:2181  --replication-factor $(replication_factor) --partitions $(partitions) --topic $(name)
run_aggregator:
	docker-compose exec jobmanager ./bin/flink run -py /opt/processor/src/aggregator.py
run_ingestor:
	docker-compose exec ingestor python main.py --scrape-interval-seconds $(ingestion_interval)