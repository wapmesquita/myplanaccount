#!/bin/bash -xe

ln -f ./src/credentials/appspot.json ./src/gac/oauth_key.json

docker run -i -t -v "$(pwd):/home/pythongae/proj" --rm=true -p 0.0.0.0:8081:8081 --name "pythongae" "pythongae/app:latest" appcfg.py -A myplancount -V $1 update /home/pythongae/proj/src/ --noauth_local_webserver
