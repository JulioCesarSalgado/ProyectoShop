#!/bin/bash

echo "Comprobando la disponibilidad del broker-1 con la IP $KAFKA_HOST y el puerto $PORT_KAFKA_HOST..."

# Esperar a que el broker-1 esté listo
until nc -z -w5 $KAFKA_HOST $PORT_KAFKA_HOST; do
    echo "$(date) - esperando a que broker-1 con la IP $KAFKA_HOST y el puerto $PORT_KAFKA_HOST esté listo..."
    sleep 2
done

echo "El broker-1 está listo. Comprobando la disponibilidad del broker-2 con la IP $KAFKA_REMOTE y el puerto $PORT_KAFKA_REMOTE..."

# Esperar a que el broker-2 esté listo
until nc -z -w5 $KAFKA_REMOTE $PORT_KAFKA_REMOTE; do
    echo "$(date) - esperando a que broker-2 con la IP $KAFKA_REMOTE y el puerto $PORT_KAFKA_REMOTE esté listo..."
    sleep 2
done

echo "El broker-2 está listo. Creando el topic..."

# Iniciar tu aplicación
python3.10 /app/crearTopic.py && echo "Terminó de crear el topic. Usando el spider..." && python3.10 /app/spiders/carso_spider.py
