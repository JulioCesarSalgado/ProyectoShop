#!/bin/bash

# Detén el servidor Kafka
docker exec -it proyectoshop-kafka-1 kafka-server-stop.sh

# Detén el servidor Zookeeper
docker exec -it proyectoshop-zookeeper-1 zkServer.sh stop

# Detén los demás servicios
docker compose down -v

# Borrar volumenes
rm -r ./Data/zookeeper_data/*
rm -r ./Data/kafka_data/*
