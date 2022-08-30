import pyautogui
from time import sleep
print(pyautogui.position())
print(pyautogui.size().width)
pyautogui.FAILSAFE=True
imageBaseDir="D:\\images\\"

def moveTo(percentX,percentY,duration):
    posX = (percentX/100) * pyautogui.size().width
    posY = (percentY/100) * pyautogui.size().height
    pyautogui.moveTo(posX,posY,duration)

pyautogui.PAUSE = 0.25
moveTo(1, 99, duration=0.5)
pyautogui.click()
pyautogui.typewrite('run')
pyautogui.typewrite(['enter'])
pyautogui.typewrite('chrome.exe --new-window https://www.udemy.com/user/logout')
pyautogui.typewrite(['enter'])

pyautogui.PAUSE = 5
pyautogui.hotkey('alt','d')
pyautogui.typewrite('https://www.udemy.com')

pyautogui.PAUSE = 5
pyautogui.typewrite(['enter'])

pyautogui.PAUSE = 0.25
pyautogui.hotkey('alt','d')
pyautogui.typewrite('https://www.udemy.com/join/login-popup?skip_suggest=1')

pyautogui.PAUSE = 5
pyautogui.typewrite(['enter'])

pyautogui.PAUSE = 0.25
moveTo(49, 45, duration=0.5)
pyautogui.click()
pyautogui.typewrite('onlineinstructorjohnhonai@gmail.com')
moveTo(44, 50, duration=0.5)
pyautogui.click()
pyautogui.hotkey('ctrl','a')
pyautogui.typewrite('Hotmail143;;')
moveTo(49, 56, duration=0.5)
pyautogui.click()

pyautogui.hotkey('alt','d')
pyautogui.typewrite('https://www.udemy.com/course/learn-android-application-development-y/learn')
pyautogui.PAUSE = 5
pyautogui.typewrite(['delete'])
pyautogui.typewrite(['enter'])

pyautogui.PAUSE = 12
searchBelowPlayButtonPosX, searchBelowPlayButtonPosY = pyautogui.locateCenterOnScreen(imageBaseDir+'SearchBelowPlayButton.png')
lowerLeftPlayerPlayButtonPosX=searchBelowPlayButtonPosX-10
lowerLeftPlayerPlayButtonPosY=searchBelowPlayButtonPosY-40

pyautogui.PAUSE = 1
moveTo((lowerLeftPlayerPlayButtonPosX/pyautogui.size().width)*100, (lowerLeftPlayerPlayButtonPosY/pyautogui.size().height)*100, duration=1)
pyautogui.click()

moveTo(94,65,1)
pyautogui.scroll(5000)

#start edit rating
moveTo(97, 12, 0.5)
pyautogui.click()
try:
    x,y=pyautogui.locateCenterOnScreen(imageBaseDir+'EditYourRating.png')
    moveTo((x/pyautogui.size().width)*100, (y/pyautogui.size().height)*100, 0.5)
    pyautogui.click()
    moveTo(60, 60, 0.5)#Edit button
    pyautogui.click()
    moveTo(56, 46, 0.5)#Star
    pyautogui.click()
    moveTo(49, 56, 0.5)#textarea
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite('Good')
    moveTo(60, 69, 0.5)#save button
    pyautogui.click()


except Exception:
    print('Unable to locate Edit Rating menu options. Looks like this is unrated')
    moveTo(78, 12, 0.5)
    pyautogui.click()
    moveTo(54, 58, 0.5)
    pyautogui.click()
    moveTo(50, 58, 0.5)
    pyautogui.click()
    pyautogui.typewrite('Good')
    moveTo(60, 69, 0.5)
    pyautogui.click()
#end edit rating

for i in range(4):
    for i in pyautogui.locateAllOnScreen(imageBaseDir+'SectionCollapse.png'):
        print (i)
        centerX = ((i.left + i.width // 2)/pyautogui.size().width) * 100
        centerY = ((i.top + i.height // 2)/pyautogui.size().height) * 100
        moveTo(centerX,centerY,0.5)
        pyautogui.click()
        sleep(0.25)
        pyautogui.scroll(5000)

for i in pyautogui.locateAllOnScreen(imageBaseDir+'SectionExpand.png'):
    print (i)
    centerX = ((i.left + i.width // 2)/pyautogui.size().width) * 100
    centerY = ((i.top + i.height // 2)/pyautogui.size().height) * 100
    moveTo(centerX, centerY, 0.5)
    pyautogui.click()
    sleep(0.25)
    print('click all checkboxes under this section')
    #click checkboxes
    for j in pyautogui.locateAllOnScreen(imageBaseDir + 'LessonCheckBox.png'):
        checkboxCenterX = ((j.left + j.width // 2)/pyautogui.size().width) * 100
        checkboxCenterY = ((j.top + j.height // 2)/pyautogui.size().height) * 100
        moveTo(checkboxCenterX, checkboxCenterY, 0.5)
        pyautogui.click()
        sleep(0.25)
    pyautogui.scroll(5000)
    centerX,centerY = pyautogui.locateCenterOnScreen(imageBaseDir+'SectionCollapse.png')
    moveTo((centerX/pyautogui.size().width)*100, (centerY/pyautogui.size().height)*100, 0.5)
    pyautogui.click()






pyautogui.hotkey('ctrl','w')
