#!/bin/bash

#Comprobación de los brokers de los servidores Kafka
python3.10 /app/comprobacion.py

# Esperar a que la bse de datos esté lista
until nc -z db_mysql 3306; do
    echo "$(date) - esperando a que la base de datos esté lista..."
    sleep 2
done

# Iniciar tu aplicación
python3.10 /app/crearTopic.py && echo "Terminó de crear el topic. Usando el spider..." && python3.10 /app/spiders/carso_spider.py
