#!/bin/bash

rm src/lib -rf 2> /dev/null
mkdir src/lib

docker run -i -t -v "$(pwd):/home/pythongae/proj" --rm=true -p 0.0.0.0:8081:8081 --name "pythongae" "pythongae/app:latest" pip install -t /home/pythongae/proj/src/lib -r /home/pythongae/proj/conf/docker/requirements.txt
