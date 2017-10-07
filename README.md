# MyPlanAccount

This is a simple guide to configure the development enviroment. Its live version is in https://myplancount.appspot.com/

## Requirements

 * Debian OS (like Ubuntu)
 * Docker

## Creating docker image

The first step is to create the docker image of the project. Just exec the following command in this folder:

    $ ./conf/docker/create-image.sh

## Starting local server

After create the docker image, just execute the command below to start the local server:

    $ ./conf/docker/run.sh

Now, the project is available on **http://localhost:8081**
