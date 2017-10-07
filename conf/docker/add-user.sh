#!/bin/bash -xe

USER="pythongae"

groupadd supersudo && echo "%supersudo ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/supersudo
adduser --disabled-password --gecos $USER $USER && usermod -a -G supersudo $USER && mkdir -p /home/$USER/.ssh
echo -e "Host github.com\n\tStrictHostKeyChecking no\n" > /home/$USER/.ssh/config
sudo chown -R $USER:$USER /home/$USER
sudo chmod 600 /home/$USER/.ssh/*
