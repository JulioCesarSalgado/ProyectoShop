#!/bin/bash

echo "Comprobando la disponibilidad del broker-1..."

# Esperar a que el broker-1 esté listo
until nc -z kafka 9092; do
    echo "$(date) - esperando a que broker-1 esté listo..."
    sleep 2
done

echo "El broker-1 está listo. Comprobando la disponibilidad del broker-2..."

# Esperar a que el broker-2 esté listo
until nc -z 192.168.1.2 9094; do
    echo "$(date) - esperando a que broker-2 esté listo..."
    sleep 2
done

echo "El broker-2 está listo. Creando el topic..."

# Iniciar tu aplicación
sudo python3.10 /app/crearTopic.py && echo "Terminó de crear el topic. Usando el spider..." && sudo python3.10 /app/spiders/carso_spider.py

