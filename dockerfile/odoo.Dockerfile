FROM odoo:latest
USER root
RUN apt update
RUN apt install curl python3-pandas nano -y
RUN pip3 install jwt