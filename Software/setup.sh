#!/bin/bash

yes | sudo apt update
yes | sudo apt full-upgrade
yes | sudo apt dist-upgrade

yes | sudo apt autoremove
yes | sudo apt clean

yes | sudo apt install python3-pip
yes | sudo apt install python3-smbus

sudo pip3 install flask
sudo pip3 install RPi.GPIO
sudo pip3 install python-dotenv
sudo pip3 install tinydb
sudo pip3 install gpiozero
sudo pip3 install smbus