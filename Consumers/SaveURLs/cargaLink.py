import os
import json
import logging
from kafka import KafkaConsumer
import mysql.connector
import time
import signal
import sys


# Crear un logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear un manejador para escribir los logs a un archivo
file_handler = logging.FileHandler('app.log')
logger.addHandler(file_handler)

# Crear un manejador para escribir los logs a stdout
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def handler(signum, frame):
    logging.info('Señal capturada, cerrando...')
    sys.exit(0)

while True:
    kafka_host = os.environ.get('KAFKA_HOST')
    port_kafka_host = os.environ.get('PORT_KAFKA_HOST')

    if kafka_host is not None and port_kafka_host is not None:
        # Las variables de entorno están disponibles, sal del bucle
        break

    logging.info("Esperando a que las variables de entorno estén disponibles...")
    time.sleep(10)

# Crear una instancia del consumidor
consumer = KafkaConsumer(bootstrap_servers=f'{kafka_host}:{port_kafka_host}', group_id='save_DB_URL')

while True:
    # Verificar si el tema existe
    if 'productos' in consumer.topics():
        consumer.subscribe(['productos'])
        break
    else:
        logging.info("El tema 'productos' no existe, reintentando en 5 segundos")
        time.sleep(5)

# Crear una conexión a la base de datos
db = mysql.connector.connect(
  host=kafka_host,
  user="usuario",
  password="ejemplo",
)

# Crear un cursor
cursor = db.cursor()

while True:
    # Verificar si la base de datos existe
    cursor.execute("SHOW DATABASES LIKE 'links'")
    result = cursor.fetchone()
    
    if result:
        # Si la base de datos existe, seleccionarla y salir del bucle
        cursor.execute("USE links")
        break
    else:
        # Si la base de datos no existe, esperar 5 segundos y luego volver a intentarlo
        print("La base de datos 'links' no existe, reintentando en 5 segundos")
        time.sleep(5)


# Consumir mensajes del topic
for message in consumer:

    # Cargar el JSON en un objeto Python
    data = json.loads(message.value.decode('utf-8'))

    # Imprimir los campos
    logging.info(f"Insertando...\nURL: {data['url']}")
    
    # Verificar si el registro ya existe en la base de datos
    cursor.execute("SELECT COUNT(*) FROM link WHERE url = %s", (data['url'],))
    count = cursor.fetchone()[0]

    if count == 0:
        # Si el registro no existe, insertarlo en la base de datos
        sql = """INSERT INTO link (url) VALUES (%s)"""
        val = (data['url'],)
        cursor.execute(sql, val)

    # Hacer commit de la transacción
    db.commit()

    # Confirmar el offset del mensaje
    consumer.commit()

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
