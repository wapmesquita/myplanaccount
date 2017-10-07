FROM ubuntu:14.04

ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir -p /home/pythongae

ADD . build_docker

RUN /build_docker/add-user.sh
RUN chown -R pythongae:pythongae /home/pythongae

RUN apt-get update
RUN apt-get install wget python unzip python-pip build-essential libssl-dev libffi-dev python-dev -y

RUN pip install -r /build_docker/requirements.txt

WORKDIR /opt
RUN wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.37.zip
RUN unzip google_appengine_1.9.37.zip
ENV PATH $PATH:/opt/google_appengine

WORKDIR /home/pythongae
USER pythongae
