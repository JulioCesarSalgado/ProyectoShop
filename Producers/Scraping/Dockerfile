FROM selenium/standalone-chrome:115.0

RUN sudo apt update -y
RUN sudo apt upgrade -y
RUN sudo apt-get install netcat -y
RUN sudo apt install software-properties-common -y
RUN sudo add-apt-repository ppa:deadsnakes/ppa -y
RUN sudo apt install python3.10 -y
RUN sudo apt install python3.10-venv python3.10-distutils -y
RUN sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN sudo python3.10 get-pip.py
RUN yes | sudo pip3.10 install selenium
RUN yes | sudo pip3.10 install pydantic
RUN yes | sudo pip3.10 install jsonlines
RUN yes | sudo pip3.10 install arrow
RUN yes | sudo pip3.10 install kafka-python
RUN yes | sudo pip3.10 install mysql-connector-python
RUN sudo rm /usr/bin/chromedriver

COPY . /app
WORKDIR /app

# Copiar el script de inicio al contenedor
COPY ./start-script.sh /start-script.sh

# Cambiar al usuario root y dar permisos de ejecución al script de inicio
USER root
RUN chmod +x /start-script.sh


CMD ["/bin/bash", "/start-script.sh"]
