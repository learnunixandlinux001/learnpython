set count=0
c:
cd c:\learnpython
:loop
set /A count=count+1
echo Run Number: %count%
C:\Python\Python39\python.exe sample.py
goto loop