#!/bin/bash

# Cargar las variables de entorno
source ../../.env

echo "Comprobando la disponibilidad del broker-1..."

# Esperar a que el broker-1 esté listo
until nc -z $KAFKA_HOST 9092; do
    echo "$(date) - esperando a que broker-1 esté listo..."
    sleep 2
done

echo "El broker-1 está listo. Comprobando la disponibilidad del broker-2..."

# Esperar a que el broker-2 esté listo
until nc -z $KAFKA_REMOTE 9094; do
    echo "$(date) - esperando a que broker-2 esté listo..."
    sleep 2
done

echo "El broker-2 está listo. Creando consumidor..."

# Iniciar tu aplicación
python3.10 /app/nomDescPrec.py

