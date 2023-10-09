#!/bin/bash

#Comprobación de los brokers de los servidores Kafka
python3.10 /app/comprobacion.py

# Iniciar tu aplicación
python3.10 /app/nomDescPrec.py

