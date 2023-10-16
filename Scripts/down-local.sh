#!/bin/bash

# Detén los demás servicios
docker compose -f docker-compose-local.yml down -v

# Borrar volumenes
for dir in "./Data_local/zookeeper_data" "./Data_local/kafka_data_1" "./Data_local/kafka_data_2" "./Data_local/mysql_data"; do
  echo "Ubicación actual: $(pwd)"
  if [ -d "$dir" ] && [ "$(ls -A $dir)" ]; then
    echo "Cambiando a directorio: $dir"
    cd "$dir"
    echo "Ubicación después de cambiar: $(pwd)"
    find . -depth -exec echo "Eliminando {} en $(pwd)" \; -exec rm -r {} \; || true
    cd -
  fi
done
