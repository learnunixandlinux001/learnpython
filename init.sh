#!/bin/bash
cd ~/Downloads
wget https://www.torproject.org/dist/torbrowser/9.0.2/tor-browser-linux64-9.0.2_en-US.tar.xz
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
mkdir ~/Downloads/tor-browser-linux64-9.0.2_en-US
tar -xvf tor-browser-linux64-9.0.2_en-US.tar.xz -C ~/Downloads/tor-browser-linux64-9.0.2_en-US  
mkdir ~/Downloads/geckodriver-v0.26.0-linux64
tar -xvf geckodriver-v0.26.0-linux64.tar.gz -C ~/Downloads/geckodriver-v0.26.0-linux64
cd ~/learnpython
echo 'UNABLE'>instance.txt
INSTANCEID=`wget -qO- http://instance-data/latest/meta-data/instance-id`
echo $INSTANCEID>instance.txt
sudo apt-get update
sudo apt update
sudo apt install -y python3
sudo apt install -y python3-pip
pip3 install selenium
pip3 install tbselenium
pip3 install pymysql
pip3 install unidecode
sudo apt install -y tor
sudo cp ~/Downloads/geckodriver-v0.26.0-linux64/geckodriver /usr/local/bin
sudo chmod 777 /usr/local/bin/geckodriver
crontab cronconfig.txt
