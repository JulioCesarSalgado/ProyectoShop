import os
from kafka.admin import KafkaAdminClient, NewTopic


kafka_host = os.getenv('KAFKA_HOST', 'localhost')

# Crear una instancia de un cliente administrativo de Kafka
admin_client = KafkaAdminClient(bootstrap_servers=f'{kafka_host}:9092')

print("Creando topico confirmación.")

# Crear una nueva instancia de topic
topic = NewTopic(name='productos', num_partitions=10, replication_factor=2)

# Crear el topic
admin_client.create_topics([topic])
