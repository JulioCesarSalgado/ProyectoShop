# Proyecto de Ingeniería de Datos

Este es un proyecto personal diseñado para demostrar habilidades en Ingeniería de Datos. El proyecto consta de varias partes que trabajan juntas para recopilar, procesar y almacenar datos.

## Descripción del Proyecto

1. **Scraping**: El proyecto comienza con un proceso de scraping que recopila información de productos de tres páginas web diferentes. Este proceso utiliza Selenium para interactuar con las páginas web y obtener los datos necesarios.

2. **Kafka**: Los datos recopilados se envían a un servidor Kafka como productor.

3. **Consumidores**: Hay tres consumidores en el proyecto:
   - El primer consumidor simplemente imprime los productos recibidos.
   - El segundo consumidor almacena las características de los productos en una base de datos MySQL.
   - El tercer consumidor almacena las URL de los productos en una base de datos MySQL.

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

Sigue estos pasos para ejecutar el proyecto:

### 1. Instalar Docker y Docker Compose
Primero, asegúrate de tener Docker y Docker Compose instalados en tu máquina. Puedes descargarlos desde la página oficial de Docker.

### 2. Clonar el repositorio
Clona el repositorio en tu máquina local utilizando el siguiente comando en tu terminal:

```git clone https://github.com/JulioCesarSalgado/ProyectoShop.git```

### 3. Iniciar los servicios con Docker Compose
Navega al directorio del proyecto:

```cd ProyectoShop```

Inicia todos los servicios utilizando Docker Compose con el siguiente comando:

```docker compose up -d```

## Licencia

(Información sobre la licencia, si corresponde)
