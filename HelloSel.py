from tbselenium.tbdriver import TorBrowserDriver
import tbselenium.common as cm
from tbselenium.utils import launch_tbb_tor_with_stem
from selenium.webdriver.common.action_chains import ActionChains
import pymysql.cursors
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from unidecode import unidecode
import random
import time
from time import sleep
import CommonCalls
import traceback

# The email for the AWS account that hosts the DB is forawsrds@gmail.com. Pass is Hotnum ('H' caps)
# We should ideally use only the free tier, so this account should not need any bill payment or any maintenance
# Just keep maintaining tables using MySQL client. You can get creds to access from MySQL by looking at the file db.txt
f = open("db.txt", "r")
hostStr = f.readline().rstrip('\n')
userStr = f.readline().rstrip('\n')
passwordStr = f.readline().rstrip('\n')
dbStr = f.readline().rstrip('\n')

# we will log the instanceid in the task table.
# When a ec2 box is setup, the instance id is populated and kept written in a file named instance.txt. Our startup scripts take care of this.
# We read it now
instfile = open("instance.txt", "r")
instanceid = instfile.readline()

# We take a separate connection in CommonCalls.py file, we don't pass the cursor along
connection = pymysql.connect(host=hostStr,
                             user=userStr,
                             password=passwordStr,
                             db=dbStr,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

# Infinite loop. Keeps going as per ratio of task allocation by RUNMODE given in configs table
while True:
    # the first search term in the list is special. It will be used to deduce the name of the credentials table for the course
    # for e.g. for the regular expressions course, the search terms are regex, regular expressions, exercises in regex etc.
    # The first term will be picked, which is regex, and it will be postfixed with _creds
    # So the table name will be deduced as regex_creds
    # For SOLID course, the first search term will be solid. So the table will be deduced as solid_creds
    sql = "SELECT `configvalue` FROM `configs` where `configname`='SPECIFICSEARCHTERMS'"
    cursor.execute(sql)
    result = cursor.fetchall()
    specificKeywordCommaSepString = result[0]['configvalue']
    specificKeywordList = specificKeywordCommaSepString.split(",")
    # FOR REFERENCE AS TO WHAT KEYWORDS APPLY TO WHICH COURSE
    # specificKeywordList = ["regex", "regular expressions", "regular expressions concepts","regular expressions exercises"]
    # specificKeywordList = ["solid","solid principles","software architecture","software design","design principles"]

    sql = "SELECT `configvalue` FROM `configs` where `configname`='TASKSPLIT'"
    allTasks = ["ENROLMENT", "ENLIST", "BROWSE", "WATCHVIDEO", "SPECIFIC", "RATING"]
    cursor.execute(sql)
    result = cursor.fetchall()
    taskSplitStr = result[0]['configvalue']
    taskSplitList = taskSplitStr.split(",")
    taskSplitList = list(map(int, taskSplitList))
    runMode = random.choices(allTasks, taskSplitList, k=1)[0]
    # runMode = 'RATING'
    print("runMode is:" + runMode)

    # for runmode RATING, dummy creds will be returned, we won't use this. For RATING, we will use some other creds decieded later on.
    (loginusername, loginpassword) = CommonCalls.getCredsForCurrentStage(runMode)
    # loginusername = 'a.modesto@aol.com'
    # loginpassword = 'm.mm00axxx'
    print("Using the creds (doesnt apply if runmode is RATING):" + loginusername + "<====>" + loginpassword)

    try:
        launch_tbb_tor_with_stem(
            "D:\\Users\\admin\\Desktop\\Tor Browser")  # I think you can remove this, but maybe some future usages need that
        driver = TorBrowserDriver("D:\\Users\\admin\\Desktop\\Tor Browser", tor_cfg=cm.USE_STEM)
        print("Created a driver successfully!")
        try:
            driver.set_page_load_timeout(10)
            driver.get("http://www.google.com")
            driver.set_page_load_timeout(40)
        except TimeoutException:
            driver.delete_all_cookies()
            driver.quit()
            sleep(5)
            continue

    except Exception:
        traceback.print_exc()

    # This will cause a browser window to open
    driver.implicitly_wait(15)

    # The login user name , password will be derived from data dump in the names table
    # Once an enrolment is completed, a record will be inserted into the creds table with the credentials.
    # creds is the master creds table, the individiual courses will also have its own creds table with user name and password.
    # So redundant creds data, but this way its easier
    if (runMode == 'ENROLMENT'):
        CommonCalls.freshSignUp(driver)
        driver.delete_all_cookies()
        driver.quit()
        sleep(10)
        # Next iteration. We are done with this. Back to the next iteration of the 'while true' loop
        continue

    if ((len(loginusername) == 0) or (len(loginpassword) == 0)):
        print("No credentials obtained for runMode:" + runMode)
        continue

    # For BROWSE, WATCHVIDEO, AND SPECIFIC modes, we will be always dealing with a single course
    # The first search term in the search terms will determin which course
    # The first search term will be used to search the course-instructors table to get the courseid
    # For RATING, we will be dealing with multiple courses
    # It is determined by the list of courses in the course-instructors table and their 'boostratio'
    try:
        if (runMode == 'BROWSE'):
            CommonCalls.login(driver, loginusername, loginpassword)
            # Browse through and enroll in 1 or 2 courses. Increase this number below if you need to.
            for i in range(random.randint(1, 2)):
                CommonCalls.memberBrowseAndEnroll(driver)
                # Not everyone who enrolls will watch immediately. So lets randomise.
                if random.choices([True, False], [10, 90], k=1)[0]:
                    CommonCalls.watchVideo(driver)

        if (runMode == 'ENLIST'):
            CommonCalls.login(driver, loginusername, loginpassword)
            CommonCalls.enlist(driver)


        if (runMode == 'WATCHVIDEO'):
            CommonCalls.login(driver, loginusername, loginpassword)
            CommonCalls.watchVideo(driver)

        if (runMode == 'SPECIFIC'):
            CommonCalls.login(driver, loginusername, loginpassword)
            CommonCalls.specificEnroll(driver, specificKeywordList, loginusername, loginpassword)

        if (runMode == 'RATING'):
            # Credentials are decided only inside the rate method.
            # Returning this loginusername from the rate method, so that a record for this can be inserted into the TASKS table.
            # Note that only the low rating task will be inserted.
            # the upgrades will not have a corresponding record in the TASKS table.
            loginusername = CommonCalls.rate(driver)

        sql = "INSERT into `tasks` values('" + loginusername + "','" + runMode + "','" + "success" + "',now(),'" + instanceid + "')"
        print("Task was successful. Using this to insert into TASKS table:::" + sql)
        cursor.execute(sql)
        connection.commit()

    except Exception as excp:
        sql = "INSERT into `tasks` values('" + loginusername + "','ERROR-" + runMode + "','" + "failed:" + traceback.format_exc().replace(
            "'", '"') + "',now(),'" + instanceid + "')"
        print("Task failed. Updating ERROR record with sql:" + sql)
        cursor.execute(sql)
        connection.commit()
    finally:
        driver.delete_all_cookies()
        driver.quit()
        sleep(10)
