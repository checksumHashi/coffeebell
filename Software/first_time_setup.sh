#!/bin/bash

yes | sudo apt update
yes | sudo apt full-upgrade
yes | sudo apt dist-upgrade

yes | sudo apt autoremove
yes | sudo apt clean

yes | sudo apt install python3-pip
yes | sudo apt install python3-smbus
yes | sudo apt install python3-venv

pip3 install flask
pip3 install RPi.GPIO
pip3 install python-dotenv
pip3 install tinydb
pip3 install gpiozero
pip3 install smbus
pip3 install gunicorn

python3 -m venv llamabell
echo "run: source llamabell/bin/activate"
echo "to turn off type deactivate"

# copy sysd service
sudo cp configfiles/coffeebell.service /etc/systemd/system/
# copy apache2 service
sudo cp configfiles/coffeebell.conf /etc/apache2/sites-available/
# create apache2 symbolic link
# (a2ensite is a part of apache2)
sudo a2ensite coffeebell.conf
sudo systemctl enable coffeebell.conf
sudo systemctl start coffeebell.conf
sudo systemctl reload apache2
