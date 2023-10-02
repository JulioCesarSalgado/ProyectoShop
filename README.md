# Proyecto de Ingeniería de Datos - *TERMINADO.*

Este es un proyecto personal diseñado para demostrar habilidades en Ingeniería de Datos. El proyecto consta de varias partes que trabajan juntas para recopilar, procesar y almacenar datos.

## Descripción del Proyecto

1. **Scraping**: El proyecto comienza con un proceso de scraping que recopila información de productos de tres páginas web diferentes.

2. **Kafka**: Los datos recopilados se envían a un servidor Kafka como productor.

3. **Consumidores**: Hay dos consumidores en el proyecto. Uno simplemente imprime los productos recibidos y el otro inserta los datos en una base de datos MySQL.

4. **Docker y Docker Compose**: Todos estos componentes se ejecutan en contenedores Docker, orquestados con Docker Compose.

## Tecnologías y Librerías Utilizadas

- Lenguaje de programación: Python
- Orquestación: Archivos SH
- Librerías Python importantes:
  - kafka-python: Para la producción y consumo de mensajes en Kafka.
  - mysql-connector-python: Para interactuar con la base de datos MySQL.
  - selenium: Para el scraping de las páginas web.
  - pydantic: Para la validación y serialización de datos.
  - jsonlines: Para trabajar con archivos JSON Lines.
  - arrow: Para manipular y formatear fechas y horas.

## Cómo Ejecutar el Proyecto

(Instrucciones para clonar el repositorio, instalar dependencias, configurar variables de entorno, etc.)

## Licencia

(Información sobre la licencia, si corresponde)
