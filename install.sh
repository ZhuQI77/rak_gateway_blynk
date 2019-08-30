#!/bin/bash

sudo apt install python3-pip python3-psycopg2 -y
sudo pip3 install blynklib

if [ ! -d paho.mqtt.python ]; then
    git clone https://github.com/eclipse/paho.mqtt.python
    push paho.mqtt.python
    sudo python3 setup.py install
    popd
fi

sudo -u postgres psql -c "create role rak_blynk with login password 'rak_blynk';"
sudo -u postgres psql -c "create database rak_blynk with owner rak_blynk;"
sudo -u postgres psql -U postgres -f init_sql.sql