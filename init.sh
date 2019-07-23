#!/bin/bash
cd ~/Downloads
wget https://www.torproject.org/dist/torbrowser/8.5.4/tor-browser-linux64-8.5.4_en-US.tar.xz
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
mkdir ~/Downloads/tor-browser-linux64-8.5.4_en-US
tar -xvf tor-browser-linux64-8.5.4_en-US.tar.xz -C ~/Downloads/tor-browser-linux64-8.5.4_en-US  
mkdir ~/Downloads/geckodriver-v0.24.0-linux64
tar -xvf geckodriver-v0.24.0-linux64.tar.gz -C ~/Downloads/geckodriver-v0.24.0-linux64
cd ~/learnpython
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
crontab cronconfig.txt
