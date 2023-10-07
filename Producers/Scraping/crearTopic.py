import os
import time
import logging
from kafka.admin import KafkaAdminClient, NewTopic

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

# Nombre del tópico
topic_name = 'productos'

logging.info("Se inició el python de creación de tema para kafka...")

while True:
    try:
        # Crear una instancia de un cliente administrativo de Kafka
        admin_client = KafkaAdminClient(bootstrap_servers=f'{kafka_host}:{port_kafka_host}')

        # Verificar si el tópico ya existe
        topics = admin_client.list_topics()
        if topic_name in topics:
            logging.info(f"El tópico {topic_name} ya existe.")
        else:
            logging.info("Creando tópico confirmación.")

            # Crear una nueva instancia de topic
            topic = NewTopic(name=topic_name, num_partitions=10, replication_factor=2)

            # Crear el topic
            admin_client.create_topics([topic])
        
        # Si todo salió bien, rompe el bucle
        break

    except NoBrokersAvailable:
        logging.info("No se pudo conectar al broker de Kafka. Reintentando en 5 segundos...")
        time.sleep(5)