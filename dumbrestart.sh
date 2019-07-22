#!/bin/bash
export DISPLAY=:0
cd ~/learnpython
pid=$(ps -ef|grep -v grep|grep HelloSel|awk '{print $2}')
echo "pid is : $pid"
if [ ! -z "$pid" ] 
then
echo "Needs a restart!"
ps -ef|grep -v grep|grep HelloSel|awk '{print $2}'|xargs kill -9
ps -ef|grep -v grep|grep tor-browser|awk '{print $2}'|xargs kill -9
echo "Dumbly killed"
echo "Starting up now...."
python3 HelloSel.py 1>logs.out 2>logs.out 0>logs.out & 
echo "...success"
fi 

