#!/bin/bash

#Comprobación de los brokers de los servidores Kafka
python3.10 /app/comprobacion.py

# Iniciar tu aplicación
python3.10 /app/crearTopic.py && echo "Terminó de crear el topic. Usando el spider..." && python3.10 /app/spiders/carso_spider.py
