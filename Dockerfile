FROM ubuntu:latest
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
MAINTAINER Steve Tsang <mylagimail2004@yahoo.com>
RUN apt-get update

RUN apt-get install --yes \
build-essential \
git-all \
python3 \
#python \
python-dev \
python-distribute \
#python-pip \
npm \
#nodejs \
unzip \
python3-pip \
wget

ENV SRC /opt
COPY Dockerfile /opt/Dockerfile

WORKDIR $SRC
RUN git clone https://github.com/stevetsa/GeneExpressionAging
WORKDIR GeneExpressionAging

WORKDIR /opt/GeneExpressionAging/webcomponents
RUN wget https://nodejs.org/dist/v6.9.1/node-v6.9.1-linux-x64.tar.xz && \
    tar -C /usr/local --strip-components 1 -xJf node*tar.xz && \
    rm node*tar.xz

#RUN npm install -g bower && \
#    echo '{ "allow_root": true, "gitUseHttps": true }' > ~/.bowerrc
RUN npm install bower
RUN npm install polymer-cli
RUN ./node_modules/bower/bin/bower install --allow-root
RUN ./node_modules/.bin/polymer build

# Expose ports
EXPOSE 8000

# Set the default command to execute
WORKDIR ../webapp
ADD ./script.sh /opt/GeneExpressionAging/
EXPOSE 8000
RUN chmod 777 /opt/GeneExpressionAging/script.sh
CMD ["/opt/GeneExpressionAging/script.sh"]
