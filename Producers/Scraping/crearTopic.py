import os
from kafka.admin import KafkaAdminClient, NewTopic

kafka_host = os.getenv('KAFKA_HOST', 'localhost')

# Crear una instancia de un cliente administrativo de Kafka
admin_client = KafkaAdminClient(bootstrap_servers=f'{kafka_host}:9092')

# Nombre del tópico que quieres crear
topic_name = 'productos'

# Verificar si el tópico ya existe
topics = admin_client.list_topics()
if topic_name in topics:
    print(f"El tópico {topic_name} ya existe.")
else:
    print("Creando tópico confirmación.")

    # Crear una nueva instancia de topic
    topic = NewTopic(name=topic_name, num_partitions=10, replication_factor=2)

    # Crear el topic
    admin_client.create_topics([topic])
