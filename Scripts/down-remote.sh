#!/bin/bash

# Detén los demás servicios
docker compose -f docker-compose-remote.yml down -v

# Borrar volumenes
for dir in "./Data_remote/zookeeper_data" "./Data_remote/kafka_data_1" "./Data_remote/mysql_data"; do
  echo "Ubicación actual: $(pwd)"
  if [ -d "$dir" ] && [ "$(ls -A $dir)" ]; then
    echo "Cambiando a directorio: $dir"
    cd "$dir"
    echo "Ubicación después de cambiar: $(pwd)"
    find . -depth -exec echo "Eliminando {} en $(pwd)" \; -exec rm -r {} \; || true
    cd -
  fi
done
