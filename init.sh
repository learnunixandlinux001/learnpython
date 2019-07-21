#!/bin/bash
sudo apt-get update
sudo apt update
sudo apt install -y python3
sudo apt install -y python3-pip
pip3 install selenium
pip3 install tbselenium
pip3 install pymysql
pip3 install unidecode
sudo apt install -y tor
sudo cp ~/Downloads/geckodriver-v0.24.0-linux64/geckodriver /usr/local/bin
sudo chmod 777 /usr/local/bin/geckodriver
