FROM python
ARG USER=ali
ENV username=${USER}
ENV password=${USER}#!
WORKDIR  /usr/src
ADD https://github.com/alishaza/ASUS-GSM-Modem/archive/refs/heads/main.zip .
RUN apt install unzip && useradd ${username} && chown ${username}:${username} -R /usr/src
USER $username
RUN unzip main.zip
USER root
WORKDIR ./ASUS-GSM-Modem-main
RUN pip install -r requirments.txt
CMD python ./REST.py
