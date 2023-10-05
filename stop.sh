#!/bin/bash

# Detén el servidor Kafka
docker exec -it proyectoshop-kafka-1 kafka-server-stop.sh

# Detén los demás servicios
docker compose stop
