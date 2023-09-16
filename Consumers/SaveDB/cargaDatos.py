import json
import logging
from kafka import KafkaConsumer
import mysql.connector
import time

# Crear un logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear un manejador para escribir los logs a un archivo
file_handler = logging.FileHandler('app.log')
logger.addHandler(file_handler)

# Crear un manejador para escribir los logs a stdout
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

# Crear una instancia del consumidor
consumer = KafkaConsumer(bootstrap_servers='192.168.1.20:9092', auto_offset_reset='earliest')

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
  host="192.168.1.20",
  user="usuario",
  password="ejemplo",
)

# Crear un cursor
cursor = db.cursor()

while True:
    # Verificar si la base de datos existe
    cursor.execute("SHOW DATABASES LIKE 'productos'")
    result = cursor.fetchone()
    
    if result:
        # Si la base de datos existe, seleccionarla y salir del bucle
        cursor.execute("USE productos")
        break
    else:
        # Si la base de datos no existe, esperar 5 segundos y luego volver a intentarlo
        print("La base de datos 'productos' no existe, reintentando en 5 segundos")
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
    
    # Insertar datos en la base de datos
    sql = """INSERT INTO producto (id, name, price, `desc`, category, specifications, pictures, date) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (data['id'], data['name'], data['price'], data['desc'], data['category'], json.dumps(data['specifications']), json.dumps(data['pictures']), data['date'])
    cursor.execute(sql, val)

    # Hacer commit de la transacción
    db.commit()