#!/bin/bash

ln -f ./src/credentials/localhost.json ./src/gac/oauth_key.json

docker rm -f "pythongae"

docker run -i -t -v "$(pwd):/home/pythongae/proj" --rm=true -p 0.0.0.0:8081:8081 --name "pythongae" "pythongae/app:latest" /home/pythongae/proj/conf/docker/up.sh
