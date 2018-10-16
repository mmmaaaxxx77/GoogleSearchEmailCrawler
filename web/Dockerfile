# VERSION 1 - EDITION 1
# !/bin/bash

FROM node:8.11

MAINTAINER johnny

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ADD . /home/node
WORKDIR /home/node/dashboard
RUN npm install -g npm@latest
RUN npm install
EXPOSE 3000
