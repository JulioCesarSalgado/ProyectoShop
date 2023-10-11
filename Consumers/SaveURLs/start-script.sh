#!/bin/bash

#Comprobación de los brokers de los servidores Kafka
python3.10 /app/comprobacion.py

# Esperar a que la bse de datos esté lista
until nc -z db_mysql 3306; do
    echo "$(date) - esperando a que la base de datos esté lista..."
    sleep 2
done



echo "La base de datos está lista. Guardando datos..."

# Iniciar tu aplicación
python3.10 /app/cargaLink.py

