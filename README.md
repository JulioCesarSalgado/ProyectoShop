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

### Preparación

Antes de ejecutar el proyecto, debes modificar el archivo `.env` con la configuración correcta:

```
KAFKA_HOST=tu_dirección_ip_del_host_de_kafka
KAFKA_REMOTE=tu_dirección_ip_remota_de_kafka
PORT_KAFKA_HOST=tu_puerto_del_host_de_kafka
PORT_KAFKA_REMOTE=tu_puerto_remoto_de_kafka
```

Para un entorno local, `KAFKA_HOST` y `KAFKA_REMOTE` deben ser la misma IP y puedes elegir cualquier puerto para `PORT_KAFKA_HOST` y `PORT_KAFKA_REMOTE`, siempre que sean diferentes.

Para un entorno remoto, `KAFKA_HOST` debe ser la IP donde se ejecuta actualmente el docker-compose y `KAFKA_REMOTE` debe ser donde está el broker remoto.

### Iniciar el Proyecto

#### Entorno Local

Para un entorno local con dos brokers de Kafka, simplemente ejecuta:

```docker-compose -f docker-compose-local.yml up -d```

Para ver los logs, puedes usar:

```docker-compose -f docker-compose-local.yml logs -f```

### Entorno Remoto

Para un entorno remoto con un broker de Kafka, sigue estos pasos:

1. Ejecuta el comando Docker Compose para iniciar los servicios:

```docker-compose -f docker-compose-remote.yml up -d```

2. Abre los logs para monitorear el estado de los servicios:

```docker-compose -f docker-compose-remote.yml logs -f```

3. Espera a que aparezcan los siguientes mensajes en los logs:

```Mon Oct 16 23:25:17 2023 - esperando a que broker con la IP (IP_KAFKA_REMOTE) y el puerto (PORT_KAFKA_REMOTE) esté listo...```

Estos mensajes provienen de los contenedores ```proyectoshop-producer_scrapy-1_remote```, ```proyectoshop-consumer_url-1_remote```, ```proyectoshop-consumer_productos-1_remote``` y ```proyectoshop-consumer_mysql-1_remote```.

4. Una vez que veas estos mensajes, inicia el broker remoto que está configurado para conectarse al zookeeper con la IP local (IP_KAFKA_LOCAL) y el puerto configurado (PORT_KAFKA_LOCAL).

### Pausar el Proyecto

#### Entorno Local

Para pausar el proyecto en un entorno local, simplemente ejecuta:

```./Scripts/stop-local.sh```

#### Entorno Remoto

Para pausar el proyecto en un entorno remoto, primero debes detener el broker remoto:

```.\bin\windows\kafka-server-stop.bat```

Luego, puedes pausar los servicios utilizando el script proporcionado:

```./Scripts/stop-remote.sh```

### Reanudar el Proyecto

Para reanudar el proyecto, ya sea en un entorno local o remoto, simplemente vuelve a ejecutar los comandos para iniciar el proyecto.

### Detener el Proyecto

#### Entorno Local

Para detener completamente el proyecto en un entorno local, simplemente ejecuta:

```./Scripts/down-local.sh```

#### Entorno Remoto

Para detener completamente el proyecto en un entorno remoto, primero debes detener el broker remoto:

```.\bin\windows\kafka-server-stop.bat```

Luego, puedes detener los servicios utilizando el script proporcionado:

```./Scripts/down-remote.sh```

## Monitoreo del Proyecto

El monitoreo es una parte crucial de cualquier proyecto de ingeniería de datos. Te permite entender el estado actual de tu sistema y te ayuda a identificar y solucionar problemas rápidamente.

### Ver los Logs

Para ver los logs del proyecto en un entorno local, puedes usar el siguiente comando:

```docker-compose -f docker-compose-local.yml logs -f```

Para un entorno remoto, el comando sería:

```docker-compose -f docker-compose-remote.yml logs -f```

### Ver el Estado de los Contenedores

Para ver el estado actual de todos los contenedores Docker, puedes usar el siguiente comando:

```docker ps -a```

Este comando te mostrará una lista de todos los contenedores, junto con su ID, imagen, comando, cuándo se crearon, estado, puertos y nombres.

### Lista de Contenedores

Aquí tienes una lista de los contenedores que existen en tu proyecto:

#### Entorno Local

- proyectoshop-kafka_2-1_local
- proyectoshop-kafka-1_local
- proyectoshop-producer_scrapy-1_local
- proyectoshop-zookeeper-1_local
- proyectoshop-consumer_mysql-1_local
- proyectoshop-consumer_url-1_local
- proyectoshop-db_mysql-1_local
- proyectoshop-consumer_productos-1_local

#### Entorno Remoto

- proyectoshop-kafka-1_remote
- proyectoshop-producer_scrapy-1_remote
- proyectoshop-zookeeper-1_remote
- proyectoshop-consumer_url-1_remote
- proyectoshop-consumer_mysql-1_remote
- proyectoshop-consumer_productos-1_remote
- proyectoshop-db_mysql-1_remote

### Entrar a un Contenedor

Para entrar a un contenedor específico, puedes usar el siguiente comando, reemplazando `nombre_del_contenedor` con el nombre del contenedor al que deseas acceder:

```docker exec -it nombre_del_contenedor /bin/bash```

Por ejemplo, para entrar al contenedor `proyectoshop-db_mysql-1_remote`, usarías:

```docker exec -it proyectoshop-db_mysql-1_remote /bin/bash```

Una vez dentro del contenedor, puedes ejecutar comandos como si estuvieras en la línea de comandos del sistema operativo del contenedor. Por ejemplo, podrías entrar al entorno MySQL para ver las tablas y demás.
