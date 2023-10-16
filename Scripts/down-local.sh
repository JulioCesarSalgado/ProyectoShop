#!/bin/bash

# Detén los demás servicios
docker compose -f docker-compose-local.yml down -v

# Borrar volumenes
for dir in "./Data_local/zookeeper_data" "./Data_local/kafka_data_1" "./Data_local/kafka_data_2" "./Data_local/mysql_data"; do
  if [ -d "$dir" ] && [ "$(ls -A $dir)" ]; then
    find "$dir" -type f -delete
  fi
done
