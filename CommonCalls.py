from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.common.action_chains import ActionChains
import pymysql.cursors
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from unidecode import unidecode
import random
from time import sleep
from datetime import datetime
import os
from math import floor
import traceback

searchKeywords = ["java", "java programming", "linux", "unix", "python", "python programming", "java", "web",
                  "internet", "blockchain", "javascript", "video", "animation", "hacking", "python coding", "coding",
                  "database", "sql", "angular", "operating system", "networking", "networks", "architecture",
                  "software", "learning", "security", "server", "nodejs", "react", "html", "css", "html5", "ios ",
                  "android apps", "data science", "cloud", "aws", "developer", "bitcoin", "html coding",
                  "python coding", "android coding", "mobile app", "selenium", "testing", "html css", "framework",
                  "spring", "artificial", "command line", "advanced", "rest api", "cisco", "certification"]

emailDomains = ["yahoo.com", "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com",
                "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
                "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk", "comcast.net", "ymail.com",
                "outlook.com", "cox.net", "rocketmail.com", "sky.com", "optonline.net", "me.com", "mail.com",
                "juno.com", "qq.com", "zoho.com", "inbox.com", "yahoo.com.br", "hotmail.com.br", "email.com",
                "pobox.com", "ygm.com", "safe-mail.net", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
                "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
                "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
                "gmail.com", "gmail.com"]

emailIdPostFixes = ["", "", "", "eng", "", "", "", "", "", "", "", "off", "", "", "", "", "", "", "", "", "study", "",
                    "", "", "", "",
                    "", "", "1", "00", "", "", "", "2000", "", "", "", "", "", "", "", "123", "", "", "66", "", "", "",
                    "", "", "",
                    "", "", "learn", "", "", "", "", "22", "", "", "", "", "", "99", "", "", "", "41", "", "work", "",
                    "", "", "", "", "1", "2", "3", "4", "5", "6", "7", "8", "9", "21", "xx", "A1", "in", "usa", ""]

emailIdMidFixes = [".", "_", "-", ".0.", "__", "-_", ".", ".", "1", ".and.", "_0_", "x", ".x1", "", ".us.", ".y."]

f2 = open("db.txt","r")
hostStr2 = f2.readline().rstrip('\n')
userStr2 = f2.readline().rstrip('\n')
passwordStr2 = f2.readline().rstrip('\n')
dbStr2 = f2.readline().rstrip('\n')

instfile = open("instance.txt","r")
#instanceid = instfile.readline()
instanceid =  os.getlogin()



connection = pymysql.connect(host=hostStr2,
                             user=userStr2,
                             password=passwordStr2,
                             db=dbStr2,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()


# pick users fit for current stage
#
#
def getCredsForCurrentStage(runMode):
    print("Entering getCredsForCurrentStage")
    try:
        sql = ""

        if (runMode == 'ENROLMENT'):
            return ("", "")

        if (runMode == 'BROWSE'):
            sql = "SELECT distinct `email` FROM `creds` where `email` NOT IN (SELECT distinct `email` FROM `tasks` where `status`='success' and `stage`='BROWSE') and `email` IN (SELECT distinct `email` FROM `tasks` where `status`='success' and `stage`='ENROLMENT') order by RAND() limit 1"

        if (runMode == 'ENLIST'):
            sql = "SELECT distinct `email` FROM `creds` where `email` NOT IN (SELECT distinct `email` FROM `tasks` where `status`='success' and `stage`='ENLIST') order by RAND() limit 1"

        if (runMode == 'WATCHVIDEO'):
            sql = "SELECT distinct `email` FROM `tasks` where `status`='success' and `stage`='BROWSE'  and `email` NOT IN (SELECT distinct `email` FROM `tasks` where `status`='success' and `stage`='WATCHVIDEO') order by RAND() limit 1"

        if (runMode == 'SPECIFIC'):
            sql = "SELECT distinct `email` FROM `creds` where `email` NOT IN (SELECT distinct `email` FROM `tasks` where `status`='success' and `stage`='SPECIFIC') order by RAND() limit 1"

        if (runMode == 'RATING'):
            sql = "SELECT distinct `email` FROM `creds` where `email` NOT IN (SELECT distinct `email` FROM `tasks` where `status`='success' and `stage`='BROWSE') order by RAND() limit 1"

        cursor.execute(sql)
        result = cursor.fetchall()
        email = result[0]['email']

        sql = "SELECT `passwd` FROM `creds` where `email`='" + email + "' order by RAND() limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        passwd = result[0]['passwd']
        print("Exited getCredsForCurrentStage")
    except Exception as e:
        print("Exception in getCredsForCurrentStage. Returning blank creds")
        return ("", "")
    return (email, passwd)


# for a fresh signup
#
#
def freshSignUp(driver):
    try:
        sql = "SELECT `firstname`, `lastname` FROM `names` order by RAND() limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()

        firstName = result[0]['firstname']
        lastName = result[0]['lastname']

        (combinedName,completeEmailId,password) = randomizeSignupData(firstName, lastName)

        print("Name:" + combinedName)
        print("Email:" + completeEmailId)
        print("Password:" + password)

        driver.get('http://www.udemy.com')
        sleep(random.randint(10, 15))
        driver.get('http://www.udemy.com')
        sleep(random.randint(10, 15))

        # Click Sign up button
        try:
            signUpButtonEl = driver.find_element_by_xpath("//button[@data-purpose='header-signup']")
            driver.execute_script("arguments[0].click();", signUpButtonEl)
        except NoSuchElementException:
            signUpNewDesignEL = driver.find_element_by_xpath('//a[contains(@href,"signup-popup")]')
            driver.execute_script("arguments[0].click();", signUpNewDesignEL)

        sleep(random.randint(6, 8))
        # Click email signup button - won't be there sometimes
        try:
            emailSignUpButtonEl = driver.find_element_by_xpath("//a[@data-purpose='email-signup-link']")
            driver.execute_script("arguments[0].click();", emailSignUpButtonEl)
            sleep(random.randint(3, 5))
        except NoSuchElementException:
            print("email signup button not there, so skipping")
        #Fill up fields and submit
        fullNameTextBoxEl = driver.find_element_by_xpath("//input[@name='fullname']")
        fullNameTextBoxEl.click()
        sleep(1)
        fullNameTextBoxEl.send_keys(combinedName)
        sleep(random.randint(2, 5))
        emailTextBoxEl = driver.find_element_by_xpath("//input[@name='email']")
        emailTextBoxEl.click()
        sleep(1)
        emailTextBoxEl.send_keys(completeEmailId)
        sleep(random.randint(2, 5))
        passwordEl = driver.find_element_by_xpath("//input[@name='password']")
        passwordEl.click()
        sleep(1)
        passwordEl.send_keys(password)
        sleep(random.randint(2, 5))
        subscribeEmailsEl = driver.find_element_by_xpath("//input[@data-purpose='subscribe-to-emails']")
        if random.choices([True, False], [85, 15], k=1)[0]:
            driver.execute_script("arguments[0].click();", subscribeEmailsEl)
            sleep(random.randint(2, 5))
        signUpSubmitButtonEl = driver.find_element_by_xpath('//input[@type="submit"]')
        signUpSubmitButtonEl.click()
        sleep(random.randint(10, 15))

        # update newly created creds into RDS
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT into `creds` values('" + combinedName + "','" + completeEmailId + "','" + password + "',now())"
        cursor.execute(sql)

        #So we update two tables, creds as well as tasks table when a single enrolment is done successfully
        sql = "INSERT into `tasks` values('" + completeEmailId + "','ENROLMENT','" + "success" + "',now(),'"+instanceid+"')"
        cursor.execute(sql)
        connection.commit()

        # Re-use the browse method. You are signed in now anyways.
        memberBrowseAndEnroll(driver)

    except Exception as excp:
        sql = "INSERT into `tasks` values('" + completeEmailId + "','ERROR-ENROLMENT','" + "failed:" + traceback.format_exc().replace(
            "'", '"') + "',now(),'"+instanceid+"')"
        print("Sql:" + sql)
        cursor.execute(sql)
        connection.commit()


# Browse through and enroll. Free filter disappeared, so might need to pick random free courses from the database of free course urls
def memberBrowseAndEnroll(driver):
    sleep(random.randint(10, 15))
    # After signinup up, search using top search field, select one results, look at one course landing page, come back
    try:
        topSearchFieldEl = driver.find_element_by_xpath('//input[contains(@id,"search-form-autocomplete")]')
        action = ActionChains(driver)
        action.move_to_element(topSearchFieldEl).click().perform()
    except NoSuchElementException:
        try:
            topSearchFieldEl = driver.find_element_by_xpath("//input[@id='header-search-field']")
            action = ActionChains(driver)
            action.move_to_element(topSearchFieldEl).click().perform()
        except NoSuchElementException:
            topSearchFieldEl = driver.find_element_by_xpath("//input[@id='header-desktop-search-bar']")
            action = ActionChains(driver)
            action.move_to_element(topSearchFieldEl).click().perform()

    sleep(1)
    topSearchFieldEl.send_keys(random.choice(searchKeywords))
    topSearchFieldEl.send_keys(Keys.RETURN)
    sleep(random.randint(10, 15))
    if random.choice([True, False]):
        try:
            nextPage = driver.find_element_by_xpath('//ul[contains(@class,"pagination")]/li/a[contains(text(),2)]')
            driver.execute_script("arguments[0].scrollIntoView();", nextPage)
            sleep(2)
            nextPage.click()
        except NoSuchElementException:
            print("Page 2 does not exist for this search")
        sleep(random.randint(10, 15))
    #basically ignore everything done till now! And directly go to a free course url picked from a database.
    #The bastards took out the free course filter button, so we can't browse and reach a free course now, have to hit URL directly.
    sql = "SELECT `courseurl` FROM `freecourses` order by rand() limit 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    editedCourseUrl = result[0]['courseurl'].replace("learn/","")
    print("going to hit free course url: "+editedCourseUrl)
    sleep(2)
    driver.get(editedCourseUrl)
    sleep(5)
    try:
        cookieOkayButton = driver.find_element_by_xpath('//div[contains(@class,"cookie-message")]/button[contains(@class,"cookie-message")]')
        driver.execute_script("arguments[0].click();", cookieOkayButton)
        print("cookie button clicked")
    except NoSuchElementException:
        try:
            print("No cookie button found")
            cookieIconButton = driver.find_element_by_xpath('//button[contains(@class,"legal-notice")]')
            driver.execute_script("arguments[0].click();", cookieIconButton)
            print("cookie icon clicked")
        except NoSuchElementException:
            print("no cookie icon found")
    try:
        enrollNowEl = driver.find_element_by_xpath("//button[@data-purpose='buy-this-course-button']")
        # driver.execute_script("arguments[0].scrollIntoView();", enrollNowEl)
        sleep(2)
        enrollNowEl.click()
        sleep(2)
    except NoSuchElementException:
        try:
            addToCartEl = driver.find_element_by_xpath("//button[contains(@class,'add-to-cart')]")
            sleep(2)
            driver.execute_script("arguments[0].scrollIntoView();", addToCartEl)
            sleep(2)
            addToCartEl.click()
            sleep(2)
            sql = "INSERT into `paidcourses` values('" + result[0]['courseurl'] + "')"
            cursor.execute(sql)
            connection.commit()
        except NoSuchElementException:
            #Some free courses migt have got paid. Need to tag it and clean up our free course data periodically
            sql = "INSERT into `paidcourses` values('" + result[0]['courseurl'] + "')"
            cursor.execute(sql)
            connection.commit()
            raise NameError("course unavailable")
    sleep(random.randint(10, 15))


def watchVideo(driver):
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))

    try:
        myCoursesTopLinkEl = driver.find_element_by_xpath('//a[contains(@href,"/home/my-courses")]')
        myCoursesTopLinkEl.click()
    except NoSuchElementException:
        myCoursesTopLinkEl = driver.find_element_by_xpath("//a[@id='header.my-learning']")
        myCoursesTopLinkEl.click()
    sleep(random.randint(10, 15))
    listOfEnrolledCourses = driver.find_elements_by_xpath('//div[contains(@class,"card")]//div[@class="play-button"]')
    numEnrolledCoursesInCurrPage = len(listOfEnrolledCourses)
    interestedEnrolledCourse = listOfEnrolledCourses[random.randint(0, numEnrolledCoursesInCurrPage - 1)]
    humanWatch(driver, interestedEnrolledCourse, '')
    firstTimeRate(driver)


# Watch video for a particular course
def humanWatch(driver, interestedEnrolledCourse, courseurl):
    if(courseurl!=''):
        driver.get("http://www.udemy.com/course/" + courseurl + "/learn")
    else:
        driver.execute_script("arguments[0].scrollIntoView();", interestedEnrolledCourse)
        try:
            dismissPopupEl = driver.find_element_by_xpath('//small[contains(@ng-click,"dismiss")]')
            dismissPopupEl.click()
            sleep(1)
        except NoSuchElementException:
            print("No angular popup in my course page found")
        # Play course!
        sleep(2)
        driver.execute_script("arguments[0].click();", interestedEnrolledCourse)
    sleep(random.randint(10, 15))
    try:
        modalPopupEl = driver.find_element_by_xpath('//div[contains(@class,"modal")]//button[@class="close"]')
        modalPopupEl.click()
        sleep(1)
    except NoSuchElementException:
        print("No modal window in course play page")
    try:
        initialPlayButton = driver.find_element_by_xpath('//div[contains(@data-purpose,"play-button")]')
        initialPlayButton.click()
    except NoSuchElementException:
        print("Play button not there on play page")
    listOfSectionExpanders = driver.find_elements_by_xpath(
        '//div[contains(@class,"section-heading")]//span[contains(@class,"angle-down")]')
    for sectionExpander in listOfSectionExpanders:
        driver.execute_script("arguments[0].scrollIntoView();", sectionExpander)
        sleep(1)
        try:
            sectionExpander.click()
        except ElementClickInterceptedException:
            print("Unable to expand section. something blocking the UI. Maybe customer care chat?")
    try:
        nextVideoRightAngler = driver.find_element_by_xpath('//span[contains(@class,"angle-right")]')
        nextVideoRightAngler.click()
    except (ElementClickInterceptedException,NoSuchElementException) as e:
        print("Right next button not present on initial video. Maybe its a quiz or coding exercise?OR maybe customer chat iframe is obscuring")
    allProgressCheckBoxes = driver.find_elements_by_xpath('//input[@data-purpose="progress-toggle-button"]')
    if(len(allProgressCheckBoxes)>101):
        allProgressCheckBoxes = allProgressCheckBoxes[0,100]

    for progressCheckBox in allProgressCheckBoxes:
        sleep(random.randint(1, 2))
        if random.choices([True, False], [80, 20], k=1)[0]:
            driver.execute_script("arguments[0].click();", progressCheckBox)
    try:
        nextVideoRightAngler = driver.find_element_by_xpath('//span[contains(@class,"angle-right")]')
        nextVideoRightAngler.click()
    except (ElementClickInterceptedException, NoSuchElementException) as e:
        print("Right next button not present on initial video. Maybe its a quiz or coding exercise?OR maybe customer chat iframe is obscuring")

def firstTimeRate(driver):
    try:
        leaveRatingEl = driver.find_element_by_xpath('//div[contains(@class,"leave-rating")]')
        driver.execute_script("arguments[0].click();", leaveRatingEl)
        sleep(2)
        ratingToBeGiven = getRatingToBeGiven(driver)
        #Rate only some courses, that is human behaviour
        if random.choices([True, False], [10, 90], k=1)[0]:
            driver.execute_script("arguments[0].click();", ratingToBeGiven)
    except NoSuchElementException:
        print("Leave rating button not found. Maybe rating already given?")


def getRatingToBeGiven(driver):
    twoEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-2-label")]')
    twoandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-2.5-label")]')
    threeEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-3-label")]')
    threeandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-3.5-label")]')
    fourEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4-label")]')
    fourandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4.5-label")]')
    fiveEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-5-label")]')

    allRatingsList = [twoEl, twoandhalfEl, threeEl, threeandhalfEl, fourEl, fourandhalfEl, fiveEl]

    sql = "SELECT `configvalue` FROM `configs` where `configname`='RATINGSPLIT'"
    cursor.execute(sql)
    result = cursor.fetchall()
    weightageSplitStr = result[0]['configvalue']
    weightageList = weightageSplitStr.split(",")
    weightageList = list(map(int, weightageList))

    ratingToBeGiven = random.choices(allRatingsList, weightageList, k=1)[0]

    return ratingToBeGiven


def login(driver, loginusername, loginpassword):
    sleep(2)
    driver.get('http://www.udemy.com')
    sleep(random.randint(5, 10))
    driver.get('http://www.udemy.com')
    sleep(random.randint(15, 20))

    try:
        cookieOkayButton = driver.find_element_by_xpath('//div[contains(@class,"cookie-message")]/button[contains(@class,"cookie-message")]')
        driver.execute_script("arguments[0].click();", cookieOkayButton)
        print("cookie button clicked")
    except NoSuchElementException:
        try:
            print("No cookie button found")
            cookieIconButton = driver.find_element_by_xpath('//button[contains(@class,"legal-notice")]')
            driver.execute_script("arguments[0].click();", cookieIconButton)
            print("cookie icon clicked")
        except NoSuchElementException:
            print("no cookie icon found")


    # Click Login button
    try:
        loginNewDesignEL = driver.find_element_by_xpath('//a[contains(@href,"login-popup")]')
        driver.execute_script("arguments[0].click();", loginNewDesignEL)
    except NoSuchElementException:
        loginButtonEl = driver.find_element_by_xpath("//button[text()='Log In']")
        driver.execute_script("arguments[0].click();", loginButtonEl)

    sleep(random.randint(10, 15))
    # Fill up username and password and submit
    emailTextBoxEl = driver.find_element_by_xpath("//input[@name='email']")
    emailTextBoxEl.click()
    sleep(1)
    emailTextBoxEl.send_keys(loginusername)
    sleep(random.randint(2, 5))
    passwordEl = driver.find_element_by_xpath("//input[@name='password']")
    passwordEl.click()
    sleep(1)
    passwordEl.send_keys(loginpassword)
    sleep(random.randint(2, 5))
    loginSubmitButtonEl = driver.find_element_by_xpath('//input[@type="submit"]')
    loginSubmitButtonEl.click()
    sleep(random.randint(10, 15))


def specificEnroll(driver, specificKeywordList, loginusername, loginpassword):
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))

    try:
        topSearchFieldEl = driver.find_element_by_xpath('//input[contains(@id,"search-form-autocomplete")]')
        action = ActionChains(driver)
        action.move_to_element(topSearchFieldEl).click().perform()
    except NoSuchElementException:
        try:
            topSearchFieldEl = driver.find_element_by_xpath("//input[@id='header-search-field']")
            action = ActionChains(driver)
            action.move_to_element(topSearchFieldEl).click().perform()
        except NoSuchElementException:
            topSearchFieldEl = driver.find_element_by_xpath("//input[@id='header-desktop-search-bar']")
            action = ActionChains(driver)
            action.move_to_element(topSearchFieldEl).click().perform()

    sleep(1)
    topSearchFieldEl.send_keys(random.choice(specificKeywordList))
    topSearchFieldEl.send_keys(Keys.RETURN)
    sleep(random.randint(10, 15))
    # Some changes to filter widget layout with the new design. Skip exec for now by setting if False below
    if random.choices([True, False], [0, 100], k=1)[0]:
        filterButtonEl = driver.find_element_by_xpath('//button[contains(@class,"filter")]/span[text()="All Filters"]')
        filterButtonEl.click()
        sleep(random.randint(2, 4))
        englishFilterEl = driver.find_element_by_xpath(
            '//span[contains(@class,"toggle-control")]//span[text()="English"]')
        sleep(random.randint(2, 4))
        driver.execute_script("arguments[0].scrollIntoView();", englishFilterEl)
        driver.execute_script("arguments[0].click();", englishFilterEl)
        try:
            freeFilterEl = driver.find_element_by_xpath('//span[contains(@class,"toggle-control")]//span[text()="Free"]')
            driver.execute_script("arguments[0].scrollIntoView();", freeFilterEl)
            driver.execute_script("arguments[0].click();", freeFilterEl)
            sleep(random.randint(2, 4))
            applyButtonEl = driver.find_element_by_xpath('//button[text()="Apply"]')
            driver.execute_script("arguments[0].scrollIntoView();", applyButtonEl)
            applyButtonEl.click()
        except NoSuchElementException:
            print("free checkbox not found")
            driver.get(driver.current_url+"&price=price-free")

        sleep(random.randint(10, 15))

    #last search term is considered the course url (after adding prefixes and postfixes added of course)
    driver.get("http://www.udemy.com/course/" + specificKeywordList[len(specificKeywordList)-1] + "/learn")
    sleep(3)
    try:
        cookieOkayButton = driver.find_element_by_xpath('//div[contains(@class,"cookie-message")]/button[contains(@class,"cookie-message")]')
        driver.execute_script("arguments[0].click();", cookieOkayButton)
        print("cookie button clicked")
    except NoSuchElementException:
        try:
            print("No cookie button found")
            cookieIconButton = driver.find_element_by_xpath('//button[contains(@class,"legal-notice")]')
            driver.execute_script("arguments[0].click();", cookieIconButton)
            print("cookie icon clicked")
        except NoSuchElementException:
            print("no cookie icon found")
    enrollNowEl = driver.find_elements_by_xpath("//button[@data-purpose='buy-this-course-button']")[0]
    sleep(3)
    enrollNowEl.click()
    sleep(random.randint(10, 15))
    #first search term is considered prefix of table name: For e.g. if first term is solid, table name is considered as solid_creds
    sql = "INSERT into `"+ specificKeywordList[0] +"_creds` values('" + loginusername + "','" + loginpassword + "','" + "unrated" + "',now(),null,null)"
    print("before inserting into course specific creds table:" + sql)
    cursor.execute(sql)
    print("after inserting into course specific creds table")
    connection.commit()

    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))


# Watch video from among enrolled courses
#
#
def watchSpecificVideoAndLeave4StarRating(driver, selectedCourseKey, courseurl):
    humanWatch(driver,'',courseurl)
    try:
        leaveRatingEl = driver.find_element_by_xpath('//div[contains(@class,"leave-rating")]')
        driver.execute_script("arguments[0].click();", leaveRatingEl)
        sleep(2)
        fourEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4-label")]')
        sleep(2)
        driver.execute_script("arguments[0].click();", fourEl)
        sleep(3)
    except NoSuchElementException:
        print("Leave rating button not found. Maybe rating already given? Try editing then")
        editRatingEl = driver.find_element_by_xpath('//span[contains(text(),"Edit your rating")]')
        driver.execute_script("arguments[0].click();", editRatingEl)
        sleep(2)
        editRatingSecondButtonEl = driver.find_element_by_xpath('//button[@data-purpose="edit-button"]')
        driver.execute_script("arguments[0].click();", editRatingSecondButtonEl)
        sleep(2)
        fourEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4-label")]')
        driver.execute_script("arguments[0].click();", fourEl)
        sleep(3)

# Upgrade ratings
#
#
def editRating(driver):
    try:
        editRatingEl = driver.find_element_by_xpath('//span[contains(text(),"Edit your rating")]')
        driver.execute_script("arguments[0].click();", editRatingEl)
        sleep(2)
        editRatingSecondButtonEl = driver.find_element_by_xpath('//button[@data-purpose="edit-button"]')
        driver.execute_script("arguments[0].click();", editRatingSecondButtonEl)
        sleep(2)
        ratingToBeGiven = getRatingToBeGiven(driver)
        driver.execute_script("arguments[0].click();", ratingToBeGiven)
        sleep(3)
    except NoSuchElementException:
        print("Edit rating button not found")


def upgradeRating(driver, selectedCourseKey, courseurl):
    humanWatch(driver, '', courseurl)
    editRating(driver)



def logout(driver):
    sleep(5)
    driver.get('http://www.udemy.com/user/logout')
    sleep(5)
    # Click Login button. TO make sure browser doesn't remember previous login, we should select 'Login as a different user'
    try:
        loginNewDesignEL = driver.find_element_by_xpath('//a[contains(@href,"login-popup")]')
        driver.execute_script("arguments[0].click();", loginNewDesignEL)
    except NoSuchElementException:
        loginButtonEl = driver.find_element_by_xpath("//button[text()='Log In']")
        driver.execute_script("arguments[0].click();", loginButtonEl)
    sleep(random.randint(10, 15))
    loginAsDifferentUserEl = driver.find_element_by_xpath("//a[@class='cancel-link']")
    driver.execute_script("arguments[0].click();", loginAsDifferentUserEl)
    sleep(2)

def rate(driver):
    sql = "SELECT `keyword`,`boostratio` FROM `course-instructors` order by keyword"
    cursor.execute(sql)
    result = cursor.fetchall()
    coursekeyList = []
    boostratioList = []
    for row in result:
        coursekey = row['keyword']
        coursekeyList.append(coursekey)
        boostratio = row['boostratio']
        boostratioList.append(boostratio)
    boostratioList = list(map(int, boostratioList))
    selectedCourseKey = random.choices(coursekeyList, boostratioList, k=1)[0]
    print("selectedCourseKey:"+selectedCourseKey)
    sql = "SELECT `instructorid`,`instructorname`,`courseurl`,`mode`,`maxdailyreviews` FROM `course-instructors` where keyword='" + selectedCourseKey + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    instructorid = result[0]['instructorid']
    instructorname = result[0]['instructorname']
    courseurl = result[0]['courseurl']
    mode = result[0]['mode']
    maxdailyreviews = result[0]['maxdailyreviews']
    print("instructorid:"+instructorid)
    print("instructorname:" + instructorname)
    print("courseurl:" + courseurl)
    print("mode:" + mode)
    print("maxdailyreviews:" + maxdailyreviews)

    #First phase. Lets upgrade a low rating from previous days if any
    sql = "SELECT `email`,`passwd` FROM `"+selectedCourseKey+"_creds` where ratingstatus='ratedlow' AND timestampdiff(DAY,lowratingdate,now())>=1 order by rand() LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        loginusername = row['email']
        loginpassword = row['passwd']
        print("upgrade rating to 4.5 or 5 for user:"+loginusername+" using passwd:"+loginpassword)
        login(driver, loginusername, loginpassword)
        upgradeRating(driver,selectedCourseKey,courseurl)
        sql = "UPDATE `" + selectedCourseKey + "_creds` set ratingstatus='upgraded', upgradedate=now() where email='" + loginusername + "'"
        print("Upgrade done, going to update rating table with:" + sql)
        cursor.execute(sql)
        connection.commit()
        logout(driver)

    #Second phase. Lets leave a 4 star rating by picking a user who has still not rated, if mode is UPGRADESONLY, skip this.
    #Max 3 reviews at a time , waiting to get upgraded. We don't want to exhaust our number of unrated bots.
    sql = "SELECT `email`,`passwd` FROM `"+selectedCourseKey+"_creds` where ratingstatus='unrated' and (select count(*) from `"+selectedCourseKey+"_creds` where ratingstatus='ratedlow')<"+maxdailyreviews+" order by rand() LIMIT 1"

    cursor.execute(sql)
    result = cursor.fetchall()

    if(len(result)==0):
        raise Exception("You have probably hit the daily review limit for now. As soon as existing low ratings get upgraded, you can push in new ratings.")
    else:
        loginusername = result[0]['email']
        loginpassword = result[0]['passwd']
    if (loginusername == ''):
        raise Exception("Unable to get rater creds")

    if (mode == 'UPGRADESONLY'):
        print("mode is UPGRADESONLY. So will not do any new ratings")
        return loginusername

    print("watch video and leave low 4 star rating for user:"+loginusername+" and passwd:"+loginpassword)
    login(driver, loginusername, loginpassword)
    watchSpecificVideoAndLeave4StarRating(driver, selectedCourseKey, courseurl)
    sql = "UPDATE `" + selectedCourseKey + "_creds` set ratingstatus='ratedlow', lowratingdate=now() where email='" + loginusername + "'"
    print("Low rating done, going to update rating table with:" + sql)
    cursor.execute(sql)
    connection.commit()
    #returning this value, so that a record for this can be inserted into the TASKS table. Note that only the low rating task will be inserted.
    # the upgrades will not have a corresponding record in the TASKS table.
    return loginusername


def enlist(driver):
    sleep(random.randint(10, 15))

    try:
        myCoursesTopLinkEl = driver.find_element_by_xpath('//a[contains(@href,"/home/my-courses")]')
        myCoursesTopLinkEl.click()
    except NoSuchElementException:
        myCoursesTopLinkEl = driver.find_element_by_xpath("//a[@id='header.my-learning']")
        myCoursesTopLinkEl.click()

    sleep(random.randint(10, 15))
    listOfEnrolledCourses = driver.find_elements_by_xpath('//a[contains(@class,"card--learning__details")]')
    numEnrolledCoursesInCurrPage = len(listOfEnrolledCourses)
    for course in listOfEnrolledCourses:
        print(course.get_attribute("href"))
        href=course.get_attribute("href")
        sql = "SELECT `courseurl` FROM `freecourses` where `courseurl`='" + href + "' limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        if (len(result)==0):
            print('inserting new free course url')
            sql = "INSERT into `freecourses` values('" + href + "')"
            cursor.execute(sql)
            connection.commit()
        else:
            print('existing free course url, will skip inserting')

#randomize signup data
def randomizeSignupData(firstName, lastName):
    # Some randomisation logic, and dealing with some special chars etc...
    firstNameAllLower = str.lower(firstName)
    firstNameFirstThree = firstNameAllLower[:2]
    firstNameFirst = firstNameAllLower[0]
    lastNameAllLower = str.lower(lastName)
    lastNameFirstThree = lastNameAllLower[:1]
    lastNameFirst = lastNameAllLower[0]
    selectedFirstNamePart = [firstNameAllLower, firstName]
    selectedLastNamePart = [lastNameAllLower, lastName]
    combinedEmailId = random.choice(selectedFirstNamePart) + random.choice(
        emailIdMidFixes) + random.choice(selectedLastNamePart) + random.choice(emailIdPostFixes)
    if (len(combinedEmailId) < 8):
        combinedEmailId = combinedEmailId + str(random.randint(10, 99))
    completeEmailId = combinedEmailId + "@" + random.choice(emailDomains)
    combinedName = random.choice(selectedFirstNamePart) + " " + random.choice(
        selectedLastNamePart)
    if (len(combinedName) < 5):
        combinedName = combinedName + firstNameAllLower
    password = random.choice(selectedLastNamePart) + random.choice(emailIdPostFixes) + random.choice(
        emailIdPostFixes) + random.choice(emailIdMidFixes)
    if (len(password) < 6):
        password = password + random.choice(selectedLastNamePart) + random.choice(
            selectedLastNamePart) + random.choice(emailIdPostFixes) + random.choice(selectedFirstNamePart) + 'abc'
    password = password.replace(" ", "")
    completeEmailId = completeEmailId.replace(" ", "")
    completeEmailId = unidecode(completeEmailId)
    password = unidecode(password)
    combinedName.replace("'", "")
    completeEmailId.replace("'", "")
    password.replace("'", "")
    return (combinedName,completeEmailId,password)
    # ...End radomisation logic

