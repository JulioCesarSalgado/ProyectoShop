from kafka import KafkaConsumer
import time
import os
import logging

# Crear un logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear un manejador para escribir los logs a un archivo
file_handler = logging.FileHandler('app.log')
logger.addHandler(file_handler)

# Crear un manejador para escribir los logs a stdout
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

kafka_host = os.environ.get('KAFKA_HOST')
port_kafka_host = os.environ.get('PORT_KAFKA_HOST')
kafka_remote = os.environ.get('KAFKA_REMOTE')
port_kafka_remote = os.environ.get('PORT_KAFKA_REMOTE')

def check_kafka_broker(kafka_host, port_kafka_host):
    bootstrap_servers = f"{kafka_host}:{port_kafka_host}"
    while True:
        try:
            consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
            logging.info(f"El broker con la IP {kafka_host} y el puerto {port_kafka_host} está listo.")
            break
        except Exception as e:
            logging.info(f"{time.ctime()} - esperando a que broker con la IP {kafka_host} y el puerto {port_kafka_host} esté listo...")
            time.sleep(10)

logging.info(f"Comprobando la disponibilidad del broker-1 con la IP {kafka_host} y el puerto {port_kafka_host}...")
check_kafka_broker(kafka_host, port_kafka_host)

logging.info(f"Comprobando la disponibilidad del broker-2 con la IP {kafka_remote} y el puerto {port_kafka_remote}...")
check_kafka_broker(kafka_remote, port_kafka_remote)

logging.info("El broker-2 está listo.")