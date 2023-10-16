#!/bin/bash

# Detén los demás servicios
docker compose -f docker-compose-remote.yml down -v

# Borrar volumenes
for dir in "./Data_remote/mysql_data" "./Data_remote/kafka_data_1" "./Data_remote/zookeeper_data"; do
  if [ -d "$dir" ] && [ "$(ls -A $dir)" ]; then
    find "$dir" -type f -delete
  fi
done
