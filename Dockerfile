FROM ubuntu:latest
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
MAINTAINER Steve Tsang <mylagimail2004@yahoo.com>
RUN apt-get update

RUN apt-get install --yes \
 build-essential \
 git-all \
 python3 \
 python \
 python-dev \
 python-distribute \
 python-pip \
 npm \
 nodejs

ENV SRC /opt

WORKDIR $SRC
RUN git clone https://github.com/stevetsa/GeneExpressionAging
RUN mkvirtualenv -p python3 GeneExpressionAging
RUN pip install -r requirements.txt
RUN mkdir data/norm_data
COPY data/normal_data.zip /data/norm_data/

# Expose ports
EXPOSE 80

# Set the default command to execute
WORKDIR $SRC/webapp
RUN workon GeneExpressionAging
CMD python manage.py runserver

COPY Dockerfile /opt/Dockerfile
