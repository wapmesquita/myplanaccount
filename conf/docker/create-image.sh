#!/bin/bash

docker rm -f "pythongae"

docker rmi "pythongae/app"

cd conf/docker

ln -s ../../src/lib lib

docker build -t "pythongae/app" .

rm lib
