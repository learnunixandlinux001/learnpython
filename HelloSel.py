from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.common.action_chains import ActionChains
import pymysql.cursors
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from unidecode import unidecode
import random
import time
from time import sleep
import CommonCalls
import traceback

f = open("db.txt","r")
hostStr = f.readline().rstrip('\n')
userStr = f.readline().rstrip('\n')
passwordStr = f.readline().rstrip('\n')
dbStr = f.readline().rstrip('\n')

instfile = open("instance.txt","r")
instanceid = instfile.readline()


connection = pymysql.connect(host=hostStr,
                             user=userStr,
                             password=passwordStr,
                             db=dbStr,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

while True:


    sql = "SELECT `configvalue` FROM `configs` where `configname`='SPECIFICSEARCHTERMS'"
    cursor.execute(sql)
    result = cursor.fetchall()
    specificKeywordCommaSepString = result[0]['configvalue']
    specificKeywordList = specificKeywordCommaSepString.split(",")


    #specificKeywordList = ["regular expressions", "regex", "regular expressions concepts","regular expressions exercises"]
    authorName = "Sujith George"


    sql = "SELECT `configvalue` FROM `configs` where `configname`='TASKSPLIT'"

    allTasks = ["ENROLMENT", "BROWSE", "WATCHVIDEO", "SPECIFIC"]

    cursor.execute(sql)
    result = cursor.fetchall()
    taskSplitStr = result[0]['configvalue']
    taskSplitList = taskSplitStr.split(",")
    taskSplitList = list(map(int, taskSplitList))

    runMode = random.choices(allTasks, taskSplitList, k=1)[0]

    #runMode = 'SPECIFIC'

    print("runMode is:" + runMode)

    (loginusername, loginpassword) = CommonCalls.getCredsForCurrentStage(runMode)

    # loginusername = 'a.modesto@aol.com'
    # loginpassword = 'm.mm00axxx'
    #print("Using the creds:"+loginusername+":::::"+loginpassword)

    try:
        driver = TorBrowserDriver("/home/ubuntu/Downloads/tor-browser-linux64-8.5.4_en-US/tor-browser_en-US")
        print("Created a driver successfully!")
    except Exception:
        traceback.print_exc()

    driver.implicitly_wait(15)

    if (runMode == 'ENROLMENT'):
        CommonCalls.freshSignUp(driver)
        driver.delete_all_cookies()
        driver.quit()
        sleep(10)
        continue

    if ((len(loginusername) == 0) or (len(loginpassword) == 0)):
        print("No credentials obtained for runMode:" + runMode)
        continue

    try:
        if (runMode == 'BROWSE'):
            CommonCalls.login(driver, loginusername, loginpassword)
            # TODO increase
            for i in range(random.randint(1, 2)):
                CommonCalls.memberBrowseAndEnroll(driver)
                if random.choices([True, False], [10, 90], k=1)[0]:
                    CommonCalls.watchVideo(driver)

        if (runMode == 'WATCHVIDEO'):
            CommonCalls.login(driver, loginusername, loginpassword)
            CommonCalls.watchVideo(driver)

        if (runMode == 'SPECIFIC'):
            CommonCalls.login(driver, loginusername, loginpassword)
            CommonCalls.specificEnroll(driver, specificKeywordList, authorName)
            CommonCalls.watchSpecificVideo(driver, authorName, loginusername)

        sql = "INSERT into `tasks` values('" + loginusername + "','" + runMode + "','" + "success" + "',now(),'"+instanceid+"')"
        print("generic success sql:" + sql)
        cursor.execute(sql)
        connection.commit()

    except Exception as excp:
        sql = "INSERT into `tasks` values('" + loginusername + "','ERROR-" + runMode + "','" + "failed:" + traceback.format_exc().replace(
            "'", '"') + "',now(),'"+instanceid+"')"
        print("generic exception catch sql:" + sql)
        cursor.execute(sql)
        connection.commit()
    finally:
        driver.delete_all_cookies()
        driver.quit()
        sleep(10)
