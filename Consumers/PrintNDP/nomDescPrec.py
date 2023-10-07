import os
import json
import logging
import time
from kafka import KafkaConsumer

# Crear un logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear un manejador para escribir los logs a un archivo
file_handler = logging.FileHandler('app.log')
logger.addHandler(file_handler)

# Crear un manejador para escribir los logs a stdout
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

while True:
    kafka_host = os.environ.get('KAFKA_HOST')
    port_kafka_host = os.environ.get('PORT_KAFKA_HOST')

    if kafka_host is not None and port_kafka_host is not None:
        # Las variables de entorno están disponibles, sal del bucle
        break

    logging.info("Esperando a que las variables de entorno estén disponibles...")
    time.sleep(10)

# Crear una instancia del consumidor
consumer = KafkaConsumer(bootstrap_servers=f'{kafka_host}:{port_kafka_host}', auto_offset_reset='latest')

while True:
    # Verificar si el tema existe
    if 'productos' in consumer.topics():
        consumer.subscribe(['productos'])
        break
    else:
        logging.info("El tema 'productos' no existe, reintentando en 5 segundos")
        time.sleep(5)

# Consumir mensajes del topic
for message in consumer:

    # Cargar el JSON en un objeto Python
    data = json.loads(message.value.decode('utf-8'))

    # Imprimir los campos
    logging.info(f"Insertando...\nID: {data['id']}")
    logging.info(f"Nombre: {data['name']}\n")
    logging.info(f"Precio: {data['price']}\n")
    logging.info(f"Descripción: {data['desc']}\n")
    logging.info(f"Categiría: {data['category']}\n")
    logging.info(f"Especificaciones: {data['specifications']}\n")
    logging.info(f"Imagenes: {data['pictures']}\n")
    logging.info(f"Fecha: {data['date']}\n")