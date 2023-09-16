# Usar una imagen base de Python
FROM python:3.10

# Instalar kafka-python
RUN pip install kafka-python

RUN apt update -y
RUN apt upgrade -y
RUN apt-get install netcat-traditional -y

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script de inicio al contenedor
COPY ./start-script.sh /start-script.sh

# Cambiar al usuario root y dar permisos de ejecución al script de inicio
USER root
RUN chmod +x /start-script.sh


CMD ["/bin/bash", "/start-script.sh"]

# Ejecutar el script de Python cuando se inicie el contenedor
#CMD ["python3.10", "nomDescPrec.py"]
